"""Validation utility functions for static analysis.

This module provides common validation functions used across different
analyzers for consistent error checking and reporting.
"""

from typing import List, Dict, Any, Optional, Union, Tuple
from pathlib import Path
import re
import logging

logger = logging.getLogger(__name__)


class ValidationUtils:
    """Utility class for common validation operations."""
    
    # Common regex patterns
    XML_NAME_PATTERN = re.compile(r'^[a-zA-Z_][\w\-\.]*$')
    URL_PATTERN = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    @staticmethod
    def validate_xml_name(name: str) -> bool:
        """Validate if a string is a valid XML name.
        
        Args:
            name: String to validate
            
        Returns:
            True if valid XML name
        """
        if not name or not isinstance(name, str):
            return False
        return bool(ValidationUtils.XML_NAME_PATTERN.match(name))
    
    @staticmethod
    def validate_url_format(url: str) -> List[str]:
        """Validate URL format and return list of issues.
        
        Args:
            url: URL string to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        if not url or not isinstance(url, str):
            errors.append("URL is empty or not a string")
            return errors
        
        url = url.strip()
        
        # Check for obvious issues
        if not url:
            errors.append("URL is empty after trimming whitespace")
            return errors
        
        if ' ' in url:
            errors.append("URL contains spaces")
        
        if url.startswith('//'):
            errors.append("URL starts with '//' (missing protocol)")
        
        if not url.startswith(('http://', 'https://', '/')):
            errors.append("URL does not start with a valid protocol or path")
        
        # Check for template variables (might be valid)
        if '{' in url and '}' in url:
            logger.debug(f"URL contains template variables: {url}")
        
        # Full regex validation (only if no obvious issues)
        if not errors and url.startswith(('http://', 'https://')):
            if not ValidationUtils.URL_PATTERN.match(url):
                errors.append("URL format is invalid")
        
        return errors
    
    @staticmethod
    def validate_file_exists(file_path: Union[str, Path]) -> Optional[str]:
        """Validate that a file exists and is readable.
        
        Args:
            file_path: Path to validate
            
        Returns:
            Error message if validation fails, None if valid
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return f"File does not exist: {path}"
            
            if not path.is_file():
                return f"Path exists but is not a file: {path}"
            
            # Try to read the file to check permissions
            try:
                with open(path, 'r') as f:
                    f.read(1)  # Read just one character
            except PermissionError:
                return f"File exists but is not readable: {path}"
            except Exception as e:
                return f"Error accessing file {path}: {str(e)}"
            
            return None
            
        except Exception as e:
            return f"Error validating file path {file_path}: {str(e)}"
    
    @staticmethod
    def validate_directory_exists(directory_path: Union[str, Path]) -> Optional[str]:
        """Validate that a directory exists and is accessible.
        
        Args:
            directory_path: Path to validate
            
        Returns:
            Error message if validation fails, None if valid
        """
        try:
            path = Path(directory_path)
            
            if not path.exists():
                return f"Directory does not exist: {path}"
            
            if not path.is_dir():
                return f"Path exists but is not a directory: {path}"
            
            # Try to list the directory to check permissions
            try:
                list(path.iterdir())
            except PermissionError:
                return f"Directory exists but is not accessible: {path}"
            except Exception as e:
                return f"Error accessing directory {path}: {str(e)}"
            
            return None
            
        except Exception as e:
            return f"Error validating directory path {directory_path}: {str(e)}"
    
    @staticmethod
    def validate_positive_integer(value: Any, name: str = "value") -> Optional[str]:
        """Validate that a value is a positive integer.
        
        Args:
            value: Value to validate
            name: Name of the value for error messages
            
        Returns:
            Error message if validation fails, None if valid
        """
        try:
            int_value = int(value)
            if int_value < 0:
                return f"{name} must be non-negative, got {int_value}"
            return None
        except (ValueError, TypeError):
            return f"{name} must be an integer, got {type(value).__name__}: {value}"
    
    @staticmethod
    def validate_threshold_config(config: Dict[str, Any]) -> List[str]:
        """Validate threshold configuration values.
        
        Args:
            config: Dictionary of threshold configuration
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        required_thresholds = [
            "max_duplicate_endpoints",
            "max_duplicate_xml_elements", 
            "max_skips_test_cases",
            "max_skips_app_modules",
            "max_skips_test_suites",
            "max_validation_errors",
            "max_validation_not_found"
        ]
        
        for threshold_name in required_thresholds:
            if threshold_name not in config:
                errors.append(f"Missing required threshold: {threshold_name}")
                continue
            
            error = ValidationUtils.validate_positive_integer(
                config[threshold_name], threshold_name
            )
            if error:
                errors.append(error)
        
        return errors
    
    @staticmethod
    def validate_file_patterns(patterns: List[str]) -> List[str]:
        """Validate file glob patterns.
        
        Args:
            patterns: List of glob patterns to validate
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        if not patterns:
            errors.append("File patterns list is empty")
            return errors
        
        for pattern in patterns:
            if not isinstance(pattern, str):
                errors.append(f"Pattern must be a string, got {type(pattern).__name__}: {pattern}")
                continue
            
            if not pattern.strip():
                errors.append("Empty pattern found in patterns list")
                continue
            
            # Check for obviously invalid patterns
            if pattern.count('*') > 2:
                logger.warning(f"Pattern has many wildcards, may be inefficient: {pattern}")
        
        return errors
    
    @staticmethod
    def sanitize_filename(filename: str, replacement: str = "_") -> str:
        """Sanitize a filename by replacing invalid characters.
        
        Args:
            filename: Original filename
            replacement: Character to replace invalid characters with
            
        Returns:
            Sanitized filename
        """
        # Characters that are invalid in filenames on most systems
        invalid_chars = r'<>:"/\|?*'
        
        sanitized = filename
        for char in invalid_chars:
            sanitized = sanitized.replace(char, replacement)
        
        # Remove or replace other problematic characters
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', replacement, sanitized)
        
        # Trim whitespace and dots from ends
        sanitized = sanitized.strip(' .')
        
        # Ensure filename is not empty and not too long
        if not sanitized:
            sanitized = "unnamed"
        
        if len(sanitized) > 255:
            sanitized = sanitized[:255]
        
        return sanitized
    
    @staticmethod
    def normalize_path_separators(path: str) -> str:
        """Normalize path separators for cross-platform compatibility.
        
        Args:
            path: Path string to normalize
            
        Returns:
            Path with normalized separators
        """
        return str(Path(path))
    
    @staticmethod
    def validate_encoding(encoding: str) -> bool:
        """Validate that an encoding is supported.
        
        Args:
            encoding: Encoding name to validate
            
        Returns:
            True if encoding is valid and supported
        """
        try:
            "test".encode(encoding).decode(encoding)
            return True
        except (LookupError, TypeError):
            return False
    
    @staticmethod
    def count_duplicates_in_list(items: List[Any]) -> Dict[Any, int]:
        """Count duplicate items in a list.
        
        Args:
            items: List of items to analyze
            
        Returns:
            Dictionary mapping items to their occurrence counts (only duplicates)
        """
        from collections import Counter
        
        counts = Counter(items)
        return {item: count for item, count in counts.items() if count > 1}
    
    @staticmethod
    def validate_configuration_completeness(config: Dict[str, Any], 
                                          required_sections: List[str]) -> List[str]:
        """Validate that configuration has all required sections.
        
        Args:
            config: Configuration dictionary
            required_sections: List of required section names
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        for section in required_sections:
            if section not in config:
                errors.append(f"Missing required configuration section: {section}")
            elif config[section] is None:
                errors.append(f"Configuration section is None: {section}")
        
        return errors