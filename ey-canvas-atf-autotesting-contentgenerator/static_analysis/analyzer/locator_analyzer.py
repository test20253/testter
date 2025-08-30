"""Analyzer for detecting direct locators in app modules and test cases.

This module validates that locators (XPATH, CSS selectors, etc.) are only defined
in XML files within the Tests/page_object folder. Direct locators found in
Tests/app_modules or Tests/test_cases are flagged as violations.
"""

import re
from typing import List, Dict, Any, Set, Tuple
from pathlib import Path
import logging

from .base_analyzer import BaseAnalyzer, AnalyzerContext
from ..parser.xml_parser import XMLParser, XMLParseError

logger = logging.getLogger(__name__)


class LocatorAnalyzer(BaseAnalyzer):
    """Analyzer for detecting direct locators outside of page object files.
    
    This analyzer ensures that locators (XPATH, CSS, etc.) are only present in 
    XML files within Tests/page_object. If locators are found in Tests/app_modules
    or Tests/test_cases, they are flagged as violations since they should use
    the <%elm:PageObjectFile:ElementName%> reference pattern instead.
    """
    
    # Parameter names that commonly contain locators
    LOCATOR_PARAMETER_NAMES = {
        'locator', 'css', 'xpath', 'element_locator', 'selector',
        'element_xpath', 'element_css', 'locator_path'
    }
    
    # Patterns that indicate direct locators (not references)
    DIRECT_LOCATOR_PATTERNS = [
        re.compile(r'^//.*'),                    # XPATH starting with //
        re.compile(r'^/.*'),                     # XPATH starting with /
        re.compile(r'^xpath:.*'),                # XPATH with xpath: prefix
        re.compile(r'^css:.*'),                  # CSS with css: prefix
        re.compile(r'^id:.*'),                   # ID with id: prefix
        re.compile(r'^name:.*'),                 # Name with name: prefix
        re.compile(r'^\[.*\]$'),                 # CSS attribute selector
        re.compile(r'^\.[\w-]+'),                # CSS class selector
        re.compile(r'^#[\w-]+'),                 # CSS ID selector
        re.compile(r'.*\[@.*\].*'),              # XPATH with attribute selector
    ]
    
    # Valid reference pattern (XML-encoded)
    VALID_REFERENCE_PATTERN = re.compile(r'^&lt;%elm:.*%&gt;$')
    
    def __init__(self, config):
        """Initialize locator analyzer.
        
        Args:
            config: Analysis configuration
        """
        super().__init__(config)
        self.xml_parser = XMLParser()
    
    def get_analyzer_name(self) -> str:
        """Get the name of this analyzer."""
        return "Locator Validation Analyzer"
    
    def get_description(self) -> str:
        """Get description of this analyzer."""
        return ("Validates that locators (XPATH, CSS, etc.) are only defined in "
                "page object files and not directly in app modules or test cases")
    
    def _perform_analysis(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Perform locator validation analysis.
        
        Args:
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings) found during analysis
        """
        errors = []
        warnings = []
        
        # Check app modules directory
        app_modules_errors = self._analyze_directory(
            self.config.directories.app_modules_dir,
            "app modules",
            context
        )
        errors.extend(app_modules_errors)
        
        # Check test cases directory  
        test_cases_errors = self._analyze_directory(
            self.config.directories.test_cases_dir,
            "test cases", 
            context
        )
        errors.extend(test_cases_errors)
        
        # Check against threshold
        total_locator_violations = len(errors)
        threshold_error = self._check_threshold(
            total_locator_violations,
            "max_direct_locators",
            self.config.thresholds.max_direct_locators,
            "direct locator violations"
        )
        if threshold_error:
            errors.append(threshold_error)
        
        return errors, warnings
    
    def _analyze_directory(self, directory: Path, directory_name: str, 
                          context: AnalyzerContext) -> List[str]:
        """Analyze all XML files in a directory for direct locators.
        
        Args:
            directory: Directory to analyze
            directory_name: Human-readable name for error reporting
            context: Analysis context
            
        Returns:
            List of error messages found
        """
        errors = []
        
        # Validate directory exists
        dir_error = self._validate_directory_exists(directory, f"{directory_name} directory")
        if dir_error:
            errors.append(dir_error)
            return errors
        
        # Get all XML files to analyze
        xml_files = self._get_files_to_analyze(directory, "*.xml")
        
        self.logger.info(f"Analyzing {len(xml_files)} XML files in {directory_name}")
        
        for xml_file in xml_files:
            try:
                file_errors = self._analyze_xml_file(xml_file, directory_name)
                errors.extend(file_errors)
                context.files_processed += 1
                
            except XMLParseError as e:
                error_msg = f"Failed to parse XML file {xml_file}: {e}"
                self.logger.warning(error_msg)
                errors.append(error_msg)
                
            except Exception as e:
                error_msg = f"Unexpected error analyzing {xml_file}: {e}"
                self.logger.error(error_msg)
                errors.append(error_msg)
        
        return errors
    
    def _analyze_xml_file(self, file_path: Path, directory_name: str) -> List[str]:
        """Analyze a single XML file for direct locators.
        
        Args:
            file_path: Path to XML file to analyze
            directory_name: Name of directory for error reporting
            
        Returns:
            List of error messages found in this file
        """
        errors = []
        
        self.logger.debug(f"Analyzing XML file: {file_path}")
        
        try:
            # Parse the XML file
            parsed_xml = self.xml_parser.parse_file(file_path)
            
            # Find all parameter elements that might contain locators
            locator_violations = self._find_locator_violations(parsed_xml, file_path)
            
            # Convert violations to error messages
            for violation in locator_violations:
                errors.append(
                    f"Direct locator found in {directory_name} file '{file_path.name}': "
                    f"parameter '{violation['parameter_name']}' contains '{violation['value']}'. "
                    f"Use <%elm:PageObjectFile:ElementName%> reference instead."
                )
                
        except Exception as e:
            # Log but don't fail the entire analysis for one file
            self.logger.warning(f"Error analyzing {file_path}: {e}")
            
        return errors
    
    def _find_locator_violations(self, xml_element, file_path: Path) -> List[Dict[str, str]]:
        """Recursively find parameter elements with direct locator violations.
        
        Args:
            xml_element: Parsed XML element to search
            file_path: Path to source file for context
            
        Returns:
            List of violation dictionaries with parameter_name and value
        """
        violations = []
        
        # Check if this is a parameter element with a locator-related name
        if (xml_element.tag == 'parameter' and 
            'name' in xml_element.attributes and
            'value' in xml_element.attributes):
            
            param_name = xml_element.attributes['name'].lower()
            param_value = xml_element.attributes['value']
            
            # Check if this parameter name suggests it might contain a locator
            if self._is_locator_parameter(param_name):
                if self._is_direct_locator(param_value):
                    violations.append({
                        'parameter_name': xml_element.attributes['name'],
                        'value': param_value
                    })
        
        # Recursively check child elements
        for child in xml_element.children:
            child_violations = self._find_locator_violations(child, file_path)
            violations.extend(child_violations)
            
        return violations
    
    def _is_locator_parameter(self, parameter_name: str) -> bool:
        """Check if a parameter name suggests it contains a locator.
        
        Args:
            parameter_name: Parameter name to check (lowercase)
            
        Returns:
            True if this parameter might contain a locator
        """
        # Check exact matches
        if parameter_name in self.LOCATOR_PARAMETER_NAMES:
            return True
            
        # Check partial matches
        locator_keywords = ['locator', 'xpath', 'css', 'selector', 'element']
        return any(keyword in parameter_name for keyword in locator_keywords)
    
    def _is_direct_locator(self, value: str) -> bool:
        """Check if a parameter value contains a direct locator.
        
        Args:
            value: Parameter value to check
            
        Returns:
            True if this appears to be a direct locator (not a valid reference)
        """
        # Skip empty values
        if not value or not value.strip():
            return False
            
        # If it matches the valid reference pattern, it's not a violation
        if self.VALID_REFERENCE_PATTERN.match(value):
            return False
            
        # Check if it matches any direct locator patterns
        for pattern in self.DIRECT_LOCATOR_PATTERNS:
            if pattern.match(value):
                return True
                
        return False
    
    def _finalize_analysis(self, context: AnalyzerContext) -> Dict[str, Any]:
        """Return metadata about the analysis.
        
        Args:
            context: Analysis context
            
        Returns:
            Dictionary of metadata
        """
        return {
            "directories_analyzed": [
                str(self.config.directories.app_modules_dir),
                str(self.config.directories.test_cases_dir)
            ],
            "locator_parameter_names": list(self.LOCATOR_PARAMETER_NAMES),
            "pattern_count": len(self.DIRECT_LOCATOR_PATTERNS)
        }