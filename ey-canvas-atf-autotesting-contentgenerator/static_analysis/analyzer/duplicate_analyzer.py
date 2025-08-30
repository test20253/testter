"""Analyzer for detecting duplicate elements across different file types.

This module provides analysis capabilities for finding duplicate endpoints,
XML elements, and other duplicated content in the Canvas automation framework.
"""

from typing import List, Dict, Any, Set, Tuple, Union
from pathlib import Path
from collections import defaultdict
import logging

from .base_analyzer import BaseAnalyzer, AnalyzerContext
from ..parser.xml_parser import XMLParser, XMLParseError
from ..parser.endpoint_parser import EndpointParser, EndpointParseError

logger = logging.getLogger(__name__)


class DuplicateAnalyzer(BaseAnalyzer):
    """Analyzer for detecting various types of duplicate content.
    
    This analyzer can detect:
    - Duplicate API endpoints in Python constant files
    - Duplicate XML elements (test cases, test suites, app modules)  
    - Duplicate keys in XML dataset files
    """
    
    def __init__(self, config):
        """Initialize duplicate analyzer.
        
        Args:
            config: Analysis configuration
        """
        super().__init__(config)
        self.xml_parser = XMLParser()
        self.endpoint_parser = EndpointParser()
    
    def get_analyzer_name(self) -> str:
        """Get the name of this analyzer."""
        return "Duplicate Content Analyzer"
    
    def get_description(self) -> str:
        """Get description of this analyzer."""
        return ("Detects duplicate API endpoints, XML elements, and dataset keys "
                "across the Canvas automation framework")
    
    def _perform_analysis(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Perform duplicate analysis across all supported file types.
        
        Args:
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings) found during analysis
        """
        errors = []
        warnings = []
        
        # Check for duplicate API endpoints
        endpoint_errors, endpoint_warnings = self._analyze_duplicate_endpoints(context)
        errors.extend(endpoint_errors)
        warnings.extend(endpoint_warnings)
        
        # Check for duplicate XML elements
        xml_errors, xml_warnings = self._analyze_duplicate_xml_elements(context)
        errors.extend(xml_errors)
        warnings.extend(xml_warnings)
        
        # Check for duplicate keys in datasets
        dataset_errors, dataset_warnings = self._analyze_duplicate_dataset_keys(context)
        errors.extend(dataset_errors)
        warnings.extend(dataset_warnings)
        
        return errors, warnings
    
    def _analyze_duplicate_endpoints(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Analyze duplicate API endpoints in Python constant files.
        
        Args:
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings) for endpoint duplicates
        """
        errors = []
        warnings = []
        
        api_dir = self.config.directories.api_constants_dir
        dir_error = self._validate_directory_exists(api_dir, "API constants directory")
        if dir_error:
            errors.append(dir_error)
            return errors, warnings
        
        try:
            # Parse all Python files in the API constants directory
            endpoint_groups = self.endpoint_parser.parse_directory(api_dir, "*.py")
            context.files_processed += len(endpoint_groups)
            
            total_duplicates = 0
            
            # Check for duplicates within each file
            for group in endpoint_groups:
                if group.duplicates:
                    file_duplicate_count = len(group.duplicates)
                    total_duplicates += file_duplicate_count
                    
                    for endpoint_value, duplicate_names in group.duplicates.items():
                        errors.append(
                            f"Duplicate endpoint value '{endpoint_value}' found in {group.file_path.name}: "
                            f"{', '.join(duplicate_names)}"
                        )
            
            # Check for duplicates across files
            global_duplicates = self.endpoint_parser.find_global_duplicates(endpoint_groups)
            for endpoint_value, endpoints in global_duplicates.items():
                if len(endpoints) > 1:
                    file_names = [ep.file_path.name for ep in endpoints]
                    endpoint_names = [ep.name for ep in endpoints]
                    
                    errors.append(
                        f"Endpoint value '{endpoint_value}' duplicated across files: "
                        f"{', '.join(f'{name}({file})' for name, file in zip(endpoint_names, file_names))}"
                    )
                    total_duplicates += 1
            
            # Check against threshold
            threshold_error = self._check_threshold(
                total_duplicates,
                "max_duplicate_endpoints",
                self.config.thresholds.max_duplicate_endpoints,
                "duplicate endpoints"
            )
            if threshold_error:
                errors.append(threshold_error)
            
            # Update context metadata
            context.metadata.update({
                "endpoint_files_processed": len(endpoint_groups),
                "total_endpoint_duplicates": total_duplicates
            })
            
        except Exception as e:
            logger.error(f"Failed to analyze duplicate endpoints: {e}")
            errors.append(f"Endpoint duplicate analysis failed: {str(e)}")
        
        return errors, warnings
    
    def _analyze_duplicate_xml_elements(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Analyze duplicate XML elements (test cases, suites, app modules).
        
        Args:
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings) for XML element duplicates
        """
        errors = []
        warnings = []
        
        # Define directories and their corresponding XML tags to check
        xml_checks = [
            (self.config.directories.test_cases_dir, "test-case", "test cases"),
            (self.config.directories.test_suites_dir, "test-suite", "test suites"),
            (self.config.directories.app_modules_dir, "app-module", "app modules")
        ]
        
        total_duplicate_files = 0
        
        for directory, tag_name, description in xml_checks:
            dir_error = self._validate_directory_exists(directory, f"{description} directory")
            if dir_error:
                warnings.append(dir_error)
                continue
            
            try:
                xml_files = self._get_files_to_analyze(directory, "*.xml")
                
                for xml_file in xml_files:
                    try:
                        # Extract element names for this tag
                        element_names = self.xml_parser.extract_attribute_values(
                            xml_file, tag_name, "name"
                        )
                        
                        # Find duplicates within this file
                        duplicates = self._find_duplicates_in_list(element_names)
                        
                        if duplicates:
                            total_duplicate_files += 1
                            for duplicate_name, count in duplicates.items():
                                errors.append(
                                    f"Duplicate {tag_name} name '{duplicate_name}' found {count} times "
                                    f"in {xml_file.name}"
                                )
                        
                        context.files_processed += 1
                        
                    except XMLParseError as e:
                        warnings.append(f"Failed to parse XML file {xml_file}: {e}")
                        continue
                        
            except Exception as e:
                logger.error(f"Failed to analyze {description}: {e}")
                warnings.append(f"Analysis of {description} failed: {str(e)}")
        
        # Check against threshold
        threshold_error = self._check_threshold(
            total_duplicate_files,
            "max_duplicate_xml_elements",
            self.config.thresholds.max_duplicate_xml_elements,
            "files with duplicate XML elements"
        )
        if threshold_error:
            errors.append(threshold_error)
        
        context.metadata.update({
            "xml_duplicate_files": total_duplicate_files
        })
        
        return errors, warnings
    
    def _analyze_duplicate_dataset_keys(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Analyze duplicate keys in XML dataset files.
        
        Args:
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings) for dataset key duplicates
        """
        errors = []
        warnings = []
        
        dataset_dir = self.config.directories.dataset_dir
        dir_error = self._validate_directory_exists(dataset_dir, "dataset directory")
        if dir_error:
            warnings.append(dir_error)
            return errors, warnings
        
        # Keys to check for duplicates
        keys_to_check = ["ID", "External_ID"]
        
        try:
            xml_files = self._get_files_to_analyze(dataset_dir, "*.xml")
            
            # Filter out excluded dataset files
            excluded_files = set(self.config.dataset_exclusions or [])
            xml_files = [f for f in xml_files if f.name not in excluded_files]
            
            for xml_file in xml_files:
                try:
                    # Get structured data from XML
                    data_dicts = self.xml_parser.get_element_data_as_dict(xml_file)
                    
                    if not data_dicts:
                        continue
                    
                    # Check each key type for duplicates
                    for key_name in keys_to_check:
                        key_values = []
                        for data_dict in data_dicts:
                            if key_name in data_dict and data_dict[key_name]:
                                key_values.append(data_dict[key_name])
                        
                        # Find duplicates for this key
                        duplicates = self._find_duplicates_in_list(key_values)
                        
                        if duplicates:
                            for duplicate_value, count in duplicates.items():
                                errors.append(
                                    f"Duplicate {key_name} '{duplicate_value}' found {count} times "
                                    f"in {xml_file.name}"
                                )
                    
                    context.files_processed += 1
                    
                except XMLParseError as e:
                    warnings.append(f"Failed to parse dataset file {xml_file}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to analyze dataset keys: {e}")
            warnings.append(f"Dataset key analysis failed: {str(e)}")
        
        return errors, warnings
    
    def _find_duplicates_in_list(self, items: List[str]) -> Dict[str, int]:
        """Find duplicate items in a list and return their counts.
        
        Args:
            items: List of items to check for duplicates
            
        Returns:
            Dictionary mapping duplicate items to their occurrence counts
        """
        item_counts = defaultdict(int)
        for item in items:
            if item:  # Skip empty items
                item_counts[item] += 1
        
        # Return only items that appear more than once
        return {item: count for item, count in item_counts.items() if count > 1}
    
    def _finalize_analysis(self, context: AnalyzerContext) -> Dict[str, Any]:
        """Finalize duplicate analysis and return metadata.
        
        Args:
            context: Analysis context
            
        Returns:
            Metadata dictionary with analysis summary
        """
        return {
            "total_files_analyzed": context.files_processed,
            "analysis_type": "duplicate_content"
        }