"""Analyzer for detecting skipped test steps and elements.

This module provides analysis capabilities for finding XML elements with skip="true"
attributes across test cases, app modules, and test suites.
"""

from typing import List, Dict, Any, Tuple
from pathlib import Path
import logging

from .base_analyzer import BaseAnalyzer, AnalyzerContext
from ..parser.xml_parser import XMLParser, XMLParseError

logger = logging.getLogger(__name__)


class SkipAnalyzer(BaseAnalyzer):
    """Analyzer for detecting skipped elements in XML test files.
    
    This analyzer scans XML files to find elements with skip="true" attributes
    and validates that the number of skipped elements doesn't exceed configured thresholds.
    """
    
    def __init__(self, config):
        """Initialize skip analyzer.
        
        Args:
            config: Analysis configuration
        """
        super().__init__(config)
        self.xml_parser = XMLParser()
    
    def get_analyzer_name(self) -> str:
        """Get the name of this analyzer."""
        return "Skip Element Analyzer"
    
    def get_description(self) -> str:
        """Get description of this analyzer."""
        return ("Detects XML elements with skip='true' attributes in test cases, "
                "app modules, and test suites, ensuring skip counts stay within thresholds")
    
    def _perform_analysis(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Perform skip analysis across all XML test directories.
        
        Args:
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings) found during analysis
        """
        errors = []
        warnings = []
        
        # Define directories to scan and their thresholds
        skip_checks = [
            (
                self.config.directories.test_cases_dir,
                "test cases",
                self.config.thresholds.max_skips_test_cases,
                "max_skips_test_cases"
            ),
            (
                self.config.directories.app_modules_dir,
                "app modules", 
                self.config.thresholds.max_skips_app_modules,
                "max_skips_app_modules"
            ),
            (
                self.config.directories.test_suites_dir,
                "test suites",
                self.config.thresholds.max_skips_test_suites,
                "max_skips_test_suites"
            )
        ]
        
        total_skips_by_category = {}
        files_with_skips_by_category = {}
        
        for directory, category, max_skips, threshold_name in skip_checks:
            dir_error = self._validate_directory_exists(directory, f"{category} directory")
            if dir_error:
                warnings.append(dir_error)
                continue
            
            try:
                category_errors, category_warnings, skip_info = self._analyze_skips_in_directory(
                    directory, category, context
                )
                
                errors.extend(category_errors)
                warnings.extend(category_warnings)
                
                total_skips = skip_info["total_skips"]
                files_with_skips = skip_info["files_with_skips"]
                
                # Store results for metadata
                total_skips_by_category[category] = total_skips
                files_with_skips_by_category[category] = files_with_skips
                
                # Check against threshold
                threshold_error = self._check_threshold(
                    total_skips,
                    threshold_name,
                    max_skips,
                    f"skipped elements in {category}"
                )
                if threshold_error:
                    errors.append(threshold_error)
                
            except Exception as e:
                logger.error(f"Failed to analyze skips in {category}: {e}")
                errors.append(f"Skip analysis failed for {category}: {str(e)}")
        
        # Update context metadata
        context.metadata.update({
            "skip_totals_by_category": total_skips_by_category,
            "files_with_skips_by_category": files_with_skips_by_category,
            "total_skips_all_categories": sum(total_skips_by_category.values())
        })
        
        return errors, warnings
    
    def _analyze_skips_in_directory(self, directory: Path, category: str, 
                                   context: AnalyzerContext) -> Tuple[List[str], List[str], Dict[str, Any]]:
        """Analyze skipped elements in a specific directory.
        
        Args:
            directory: Directory to analyze
            category: Human-readable category name
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings, skip_info_dict)
        """
        errors = []
        warnings = []
        
        xml_files = self._get_files_to_analyze(directory, "*.xml")
        total_skips = 0
        files_with_skips = {}
        
        for xml_file in xml_files:
            try:
                skip_count = self._count_skips_in_file(xml_file)
                
                if skip_count > 0:
                    files_with_skips[xml_file.name] = skip_count
                    total_skips += skip_count
                    
                    # Log detailed information about files with skips
                    self.logger.debug(f"Found {skip_count} skipped elements in {xml_file.name}")
                
                context.files_processed += 1
                
            except XMLParseError as e:
                warnings.append(f"Failed to parse {category} file {xml_file.name}: {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error processing {xml_file}: {e}")
                warnings.append(f"Error processing {xml_file.name}: {str(e)}")
                continue
        
        skip_info = {
            "total_skips": total_skips,
            "files_with_skips": files_with_skips,
            "files_analyzed": len(xml_files)
        }
        
        return errors, warnings, skip_info
    
    def _count_skips_in_file(self, file_path: Path) -> int:
        """Count the number of elements with skip="true" in an XML file.
        
        Args:
            file_path: Path to the XML file to analyze
            
        Returns:
            Number of elements with skip="true" attribute
            
        Raises:
            XMLParseError: If the file cannot be parsed
        """
        root_element = self.xml_parser.parse_file(file_path)
        return self._count_skips_recursive(root_element)
    
    def _count_skips_recursive(self, element) -> int:
        """Recursively count skip="true" attributes in an XML element tree.
        
        Args:
            element: XMLElement to analyze
            
        Returns:
            Total count of skip="true" attributes in this element and its children
        """
        skip_count = 0
        
        # Check if this element has skip="true"
        if element.attributes.get("skip") == "true":
            skip_count += 1
        
        # Recursively check children
        for child in element.children:
            skip_count += self._count_skips_recursive(child)
        
        return skip_count
    
    def _finalize_analysis(self, context: AnalyzerContext) -> Dict[str, Any]:
        """Finalize skip analysis and return metadata.
        
        Args:
            context: Analysis context
            
        Returns:
            Metadata dictionary with analysis summary
        """
        return {
            "total_files_analyzed": context.files_processed,
            "analysis_type": "skip_elements"
        }