"""Endpoint parsing utilities for API constant files.

This module provides parsing capabilities for extracting and analyzing
API endpoints from Python constant files.
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Union
from collections import defaultdict
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class EndpointParseError(Exception):
    """Exception raised when endpoint parsing fails."""
    
    def __init__(self, file_path: Union[str, Path], error_message: str):
        self.file_path = Path(file_path)
        self.error_message = error_message
        super().__init__(f"Failed to parse endpoints from '{self.file_path}': {error_message}")


@dataclass
class Endpoint:
    """Represents a parsed API endpoint.
    
    Attributes:
        name: Variable name of the endpoint
        value: URL value of the endpoint (normalized to lowercase)
        original_value: Original URL value before normalization
        file_path: Path to the source file
        line_number: Line number where the endpoint was found
    """
    name: str
    value: str
    original_value: str
    file_path: Path
    line_number: Optional[int] = None


@dataclass
class EndpointGroup:
    """Represents a collection of endpoints from a single file.
    
    Attributes:
        file_path: Path to the source file
        endpoints: List of endpoints found in the file
        duplicates: Dictionary mapping endpoint values to lists of duplicate names
    """
    file_path: Path
    endpoints: List[Endpoint]
    duplicates: Dict[str, List[str]]


class EndpointParser:
    """Parser for extracting API endpoints from Python constant files.
    
    This parser uses regular expressions to find endpoint definitions
    in Python files and can detect duplicate endpoint values.
    """
    
    # Pattern to match endpoint assignments like: self._endpoint = "value" or ENDPOINT = "value"
    ENDPOINT_PATTERN = re.compile(
        r"(self\._\w+|\w+)\s*=\s*['\"]([^'\"]*)['\"]",
        re.MULTILINE
    )
    
    def __init__(self, normalize_values: bool = True):
        """Initialize endpoint parser.
        
        Args:
            normalize_values: Whether to normalize endpoint values to lowercase for comparison
        """
        self.normalize_values = normalize_values
    
    def parse_file(self, file_path: Union[str, Path], encoding: str = "utf-8") -> EndpointGroup:
        """Parse endpoints from a Python file.
        
        Args:
            file_path: Path to the Python file to parse
            encoding: File encoding to use
            
        Returns:
            EndpointGroup containing all found endpoints and duplicates
            
        Raises:
            EndpointParseError: If the file cannot be parsed
            FileNotFoundError: If the file does not exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Endpoint file not found: {file_path}")
        
        logger.debug(f"Parsing endpoints from file: {file_path}")
        
        try:
            with open(file_path, "r", encoding=encoding) as file:
                content = file.read()
        except Exception as e:
            raise EndpointParseError(file_path, f"Could not read file: {str(e)}")
        
        endpoints = self._extract_endpoints(content, file_path)
        duplicates = self._find_duplicates(endpoints)
        
        return EndpointGroup(
            file_path=file_path,
            endpoints=endpoints,
            duplicates=duplicates
        )
    
    def parse_directory(self, directory_path: Union[str, Path], 
                       file_pattern: str = "*.py") -> List[EndpointGroup]:
        """Parse endpoints from all Python files in a directory.
        
        Args:
            directory_path: Path to directory containing Python files
            file_pattern: Glob pattern for matching files
            
        Returns:
            List of EndpointGroup objects, one per file
            
        Raises:
            FileNotFoundError: If the directory does not exist
        """
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        if not directory_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        python_files = list(directory_path.glob(file_pattern))
        endpoint_groups = []
        
        for file_path in python_files:
            try:
                group = self.parse_file(file_path)
                endpoint_groups.append(group)
            except (EndpointParseError, FileNotFoundError) as e:
                logger.warning(f"Failed to parse {file_path}: {e}")
                continue
        
        return endpoint_groups
    
    def find_global_duplicates(self, endpoint_groups: List[EndpointGroup]) -> Dict[str, List[Endpoint]]:
        """Find duplicate endpoint values across multiple files.
        
        Args:
            endpoint_groups: List of endpoint groups to analyze
            
        Returns:
            Dictionary mapping endpoint values to lists of endpoints with that value
        """
        value_to_endpoints = defaultdict(list)
        
        for group in endpoint_groups:
            for endpoint in group.endpoints:
                value_to_endpoints[endpoint.value].append(endpoint)
        
        # Filter to only include values that appear multiple times
        return {
            value: endpoints 
            for value, endpoints in value_to_endpoints.items()
            if len(endpoints) > 1
        }
    
    def get_all_endpoint_names(self, endpoint_groups: List[EndpointGroup]) -> Set[str]:
        """Get all unique endpoint names across all groups.
        
        Args:
            endpoint_groups: List of endpoint groups to analyze
            
        Returns:
            Set of all unique endpoint names
        """
        names = set()
        for group in endpoint_groups:
            for endpoint in group.endpoints:
                names.add(endpoint.name)
        return names
    
    def get_all_endpoint_values(self, endpoint_groups: List[EndpointGroup]) -> Set[str]:
        """Get all unique endpoint values across all groups.
        
        Args:
            endpoint_groups: List of endpoint groups to analyze
            
        Returns:
            Set of all unique endpoint values
        """
        values = set()
        for group in endpoint_groups:
            for endpoint in group.endpoints:
                values.add(endpoint.value)
        return values
    
    def validate_endpoint_format(self, endpoint: Endpoint) -> List[str]:
        """Validate the format of an endpoint URL.
        
        Args:
            endpoint: Endpoint to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        value = endpoint.original_value
        
        # Check for empty values
        if not value.strip():
            errors.append("Endpoint value is empty")
            return errors
        
        # Check for common URL issues
        if " " in value:
            errors.append("Endpoint value contains spaces")
        
        if value.startswith("//"):
            errors.append("Endpoint value starts with '//' (missing protocol)")
        
        # Check for suspicious patterns
        if "{" in value and "}" in value:
            # This might be a template URL, which could be valid
            logger.debug(f"Endpoint {endpoint.name} appears to be a template URL")
        
        return errors
    
    def _extract_endpoints(self, content: str, file_path: Path) -> List[Endpoint]:
        """Extract endpoints from file content using regex pattern matching."""
        endpoints = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            matches = self.ENDPOINT_PATTERN.findall(line)
            
            for endpoint_name, endpoint_value in matches:
                normalized_value = endpoint_value.lower() if self.normalize_values else endpoint_value
                
                endpoint = Endpoint(
                    name=endpoint_name,
                    value=normalized_value,
                    original_value=endpoint_value,
                    file_path=file_path,
                    line_number=line_num
                )
                endpoints.append(endpoint)
        
        return endpoints
    
    def _find_duplicates(self, endpoints: List[Endpoint]) -> Dict[str, List[str]]:
        """Find duplicate endpoint values within a list of endpoints."""
        value_to_names = defaultdict(list)
        
        for endpoint in endpoints:
            value_to_names[endpoint.value].append(endpoint.name)
        
        # Return only values that have multiple names
        return {
            value: names
            for value, names in value_to_names.items()
            if len(names) > 1
        }