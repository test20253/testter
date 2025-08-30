"""Analyzer for validating test case references and dependencies.

This module provides analysis capabilities for validating that test case references
in test suites actually exist and can be resolved correctly.
"""

from typing import List, Dict, Any, Tuple, Set, Optional, Union
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from .base_analyzer import BaseAnalyzer, AnalyzerContext
from ..parser.xml_parser import XMLParser, XMLParseError

logger = logging.getLogger(__name__)


class ReferenceAnalyzer(BaseAnalyzer):
    """Analyzer for validating test case references in test suites.
    
    This analyzer ensures that all test case references in test suite XML files
    point to valid, existing test cases and validates the integrity of the
    test framework structure.
    """
    
    # Status constants for test case validation
    STATUS_FOUND = "Found"
    STATUS_NOT_FOUND = "Test Not Found"
    STATUS_FILE_NOT_FOUND = "Test File Not Found"
    STATUS_XML_PARSE_ERROR = "XML Parse Error"
    
    def __init__(self, config):
        """Initialize reference analyzer.
        
        Args:
            config: Analysis configuration
        """
        super().__init__(config)
        self.xml_parser = XMLParser()
        self._test_file_cache: Dict[Path, Set[str]] = {}
    
    def get_analyzer_name(self) -> str:
        """Get the name of this analyzer."""
        return "Test Reference Analyzer"
    
    def get_description(self) -> str:
        """Get description of this analyzer."""
        return ("Validates that all test case references in test suites point to "
                "existing test cases and checks for broken dependencies")
    
    def _perform_analysis(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Perform reference validation across all test suites.
        
        Args:
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings) found during analysis
        """
        errors = []
        warnings = []
        
        # Validate directories exist
        suites_dir = self.config.directories.test_suites_dir
        cases_dir = self.config.directories.test_cases_dir
        
        suites_error = self._validate_directory_exists(suites_dir, "test suites directory")
        cases_error = self._validate_directory_exists(cases_dir, "test cases directory")
        
        if suites_error:
            errors.append(suites_error)
        if cases_error:
            errors.append(cases_error)
            
        if errors:
            return errors, warnings
        
        try:
            # Get all test suite files
            suite_files = self._get_files_to_analyze(suites_dir, "*.xml")
            
            if not suite_files:
                warnings.append("No test suite files found to analyze")
                return errors, warnings
            
            # Analyze each test suite (can be parallelized for large codebases)
            all_results = []
            
            # Use ThreadPoolExecutor for concurrent processing
            with ThreadPoolExecutor(max_workers=4) as executor:
                future_to_suite = {
                    executor.submit(self._analyze_test_suite, suite_file): suite_file
                    for suite_file in suite_files
                }
                
                for future in as_completed(future_to_suite):
                    suite_file = future_to_suite[future]
                    try:
                        suite_results = future.result()
                        all_results.extend(suite_results)
                        context.files_processed += 1
                    except Exception as e:
                        logger.error(f"Failed to analyze suite {suite_file}: {e}")
                        errors.append(f"Failed to analyze test suite {suite_file.name}: {str(e)}")
            
            # Process results and generate errors/warnings
            reference_errors, reference_warnings = self._process_validation_results(all_results)
            errors.extend(reference_errors)
            warnings.extend(reference_warnings)
            
            # Update context metadata
            context.metadata.update({
                "suite_files_analyzed": len(suite_files),
                "total_references_checked": len(all_results),
                "validation_results": self._summarize_results(all_results)
            })
            
        except Exception as e:
            logger.error(f"Reference analysis failed: {e}")
            errors.append(f"Reference validation failed: {str(e)}")
        
        return errors, warnings
    
    def _analyze_test_suite(self, suite_file: Path) -> List[Tuple[str, str, str, str]]:
        """Analyze a single test suite file for test case references.
        
        Args:
            suite_file: Path to the test suite XML file
            
        Returns:
            List of tuples (suite_file, test_file, test_case, status)
        """
        results = []
        
        try:
            # Parse test suite and extract test case references
            test_cases = self._extract_test_case_references(suite_file)
            
            for test_file, test_case_name in test_cases:
                # Validate each test case reference
                status = self._validate_test_case_exists(test_file, test_case_name)
                results.append((str(suite_file), test_file, test_case_name, status))
                
        except XMLParseError as e:
            logger.warning(f"Failed to parse test suite {suite_file}: {e}")
            results.append((str(suite_file), "", "", self.STATUS_XML_PARSE_ERROR))
        
        return results
    
    def _extract_test_case_references(self, suite_file: Path) -> List[Tuple[str, str]]:
        """Extract test case references from a test suite XML file.
        
        Args:
            suite_file: Path to the test suite XML file
            
        Returns:
            List of tuples (test_file, test_case_name)
        """
        test_cases = []
        
        # Parse the XML and look for test-case elements
        elements = self.xml_parser.extract_elements_by_tag(suite_file, "test-case")
        
        for element in elements:
            test_file = element.attributes.get("test-case-file", "")
            test_case_name = element.attributes.get("test-case-name", "")
            
            if test_file and test_case_name:
                test_cases.append((test_file, test_case_name))
        
        return test_cases
    
    def _validate_test_case_exists(self, test_file: str, test_case_name: str) -> str:
        """Validate that a specific test case exists in the referenced file.
        
        Args:
            test_file: Name of the test case file (may or may not include .xml)
            test_case_name: Name of the test case to find
            
        Returns:
            Status string indicating the validation result
        """
        # Load test cases from the file (with caching)
        test_cases = self._load_test_cases_from_file(test_file)
        
        if isinstance(test_cases, str):
            # Error status returned from loading
            return test_cases
        
        # Check if the test case exists
        return self.STATUS_FOUND if test_case_name in test_cases else self.STATUS_NOT_FOUND
    
    def _load_test_cases_from_file(self, test_file: str) -> Union[Set[str], str]:
        """Load test cases from a test case XML file with caching.
        
        Args:
            test_file: Name of the test case file
            
        Returns:
            Set of test case names or error status string
        """
        cases_dir = self.config.directories.test_cases_dir
        
        # Try as given first
        full_path = cases_dir / test_file
        
        # If file doesn't exist and doesn't end with .xml, try adding .xml
        if not full_path.exists() and not test_file.lower().endswith('.xml'):
            full_path = cases_dir / f"{test_file}.xml"
        
        # Check cache first
        if full_path in self._test_file_cache:
            return self._test_file_cache[full_path]
        
        if not full_path.exists():
            return self.STATUS_FILE_NOT_FOUND
        
        try:
            # Extract test case names
            test_case_names = set(
                self.xml_parser.extract_attribute_values(full_path, "test-case", "name")
            )
            
            # Cache the result
            self._test_file_cache[full_path] = test_case_names
            return test_case_names
            
        except XMLParseError:
            return self.STATUS_XML_PARSE_ERROR
    
    def _process_validation_results(self, results: List[Tuple[str, str, str, str]]) -> Tuple[List[str], List[str]]:
        """Process validation results and generate error/warning messages.
        
        Args:
            results: List of validation result tuples
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        
        # Count different types of results
        not_found_count = 0
        error_count = 0
        
        for suite_file, test_file, test_case, status in results:
            if status == self.STATUS_NOT_FOUND:
                not_found_count += 1
                errors.append(
                    f"Test case '{test_case}' not found in file '{test_file}' "
                    f"(referenced in {Path(suite_file).name})"
                )
            elif status == self.STATUS_FILE_NOT_FOUND:
                error_count += 1
                errors.append(
                    f"Test case file '{test_file}' not found "
                    f"(referenced in {Path(suite_file).name})"
                )
            elif status == self.STATUS_XML_PARSE_ERROR:
                error_count += 1
                warnings.append(
                    f"Failed to parse test file '{test_file}' "
                    f"(referenced in {Path(suite_file).name})"
                )
        
        # Check against thresholds
        not_found_error = self._check_threshold(
            not_found_count,
            "max_validation_not_found",
            self.config.thresholds.max_validation_not_found,
            "missing test case references"
        )
        if not_found_error:
            errors.append(not_found_error)
            
        error_threshold_error = self._check_threshold(
            error_count,
            "max_validation_errors",
            self.config.thresholds.max_validation_errors,
            "test reference validation errors"
        )
        if error_threshold_error:
            errors.append(error_threshold_error)
        
        return errors, warnings
    
    def _summarize_results(self, results: List[Tuple[str, str, str, str]]) -> Dict[str, int]:
        """Summarize validation results for metadata.
        
        Args:
            results: List of validation result tuples
            
        Returns:
            Dictionary with result counts by status
        """
        summary = {
            "total_references": len(results),
            "found": 0,
            "not_found": 0,
            "file_not_found": 0,
            "parse_errors": 0
        }
        
        for _, _, _, status in results:
            if status == self.STATUS_FOUND:
                summary["found"] += 1
            elif status == self.STATUS_NOT_FOUND:
                summary["not_found"] += 1
            elif status == self.STATUS_FILE_NOT_FOUND:
                summary["file_not_found"] += 1
            elif status == self.STATUS_XML_PARSE_ERROR:
                summary["parse_errors"] += 1
        
        return summary
    
    def _finalize_analysis(self, context: AnalyzerContext) -> Dict[str, Any]:
        """Finalize reference analysis and clear caches.
        
        Args:
            context: Analysis context
            
        Returns:
            Metadata dictionary with analysis summary
        """
        # Clear the test file cache to free memory
        cache_size = len(self._test_file_cache)
        self._test_file_cache.clear()
        
        return {
            "total_files_analyzed": context.files_processed,
            "analysis_type": "test_references",
            "cache_entries_cleared": cache_size
        }