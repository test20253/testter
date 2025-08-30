"""XML parsing utilities for static analysis.

This module provides robust XML parsing capabilities with proper error handling,
caching, and support for various XML structures used in the Canvas automation framework.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Set, Optional, Any, Union
import logging
from dataclasses import dataclass
from threading import Lock
import time

logger = logging.getLogger(__name__)


class XMLParseError(Exception):
    """Exception raised when XML parsing fails."""
    
    def __init__(self, file_path: Union[str, Path], error_message: str):
        self.file_path = Path(file_path)
        self.error_message = error_message
        super().__init__(f"Failed to parse XML file '{self.file_path}': {error_message}")


@dataclass
class XMLElement:
    """Represents a parsed XML element with metadata.
    
    Attributes:
        tag: The XML tag name
        attributes: Dictionary of XML attributes  
        text: Text content of the element
        children: List of child XMLElement objects
        file_path: Path to the source XML file
        line_number: Line number in source file (if available)
    """
    tag: str
    attributes: Dict[str, str]
    text: Optional[str]
    children: List['XMLElement']
    file_path: Path
    line_number: Optional[int] = None


class XMLParser:
    """Thread-safe XML parser with caching and error handling.
    
    This parser provides a consistent interface for parsing XML files
    used throughout the Canvas automation framework.
    """
    
    def __init__(self, cache_enabled: bool = True, cache_max_size: int = 100):
        """Initialize XML parser.
        
        Args:
            cache_enabled: Whether to cache parsed XML files
            cache_max_size: Maximum number of files to cache
        """
        self._cache_enabled = cache_enabled
        self._cache_max_size = cache_max_size
        self._cache: Dict[Path, XMLElement] = {}
        self._cache_timestamps: Dict[Path, float] = {}
        self._cache_lock = Lock()
        
    def parse_file(self, file_path: Union[str, Path], encoding: str = "utf-8") -> XMLElement:
        """Parse an XML file and return structured data.
        
        Args:
            file_path: Path to the XML file to parse
            encoding: File encoding to use
            
        Returns:
            Parsed XML element tree
            
        Raises:
            XMLParseError: If the file cannot be parsed
            FileNotFoundError: If the file does not exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"XML file not found: {file_path}")
            
        # Check cache first
        if self._cache_enabled:
            cached_element = self._get_from_cache(file_path)
            if cached_element is not None:
                logger.debug(f"Using cached XML parse result for {file_path}")
                return cached_element
        
        logger.debug(f"Parsing XML file: {file_path}")
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            parsed_element = self._convert_element(root, file_path)
            
            # Cache the result
            if self._cache_enabled:
                self._add_to_cache(file_path, parsed_element)
                
            return parsed_element
            
        except ET.ParseError as e:
            raise XMLParseError(file_path, str(e))
        except Exception as e:
            raise XMLParseError(file_path, f"Unexpected error: {str(e)}")
    
    def extract_elements_by_tag(self, file_path: Union[str, Path], tag_name: str) -> List[XMLElement]:
        """Extract all elements with a specific tag from an XML file.
        
        Args:
            file_path: Path to the XML file
            tag_name: XML tag name to search for
            
        Returns:
            List of elements matching the tag name
        """
        root_element = self.parse_file(file_path)
        return self._find_elements_by_tag(root_element, tag_name)
    
    def extract_attribute_values(self, file_path: Union[str, Path], 
                                tag_name: str, attribute_name: str) -> List[str]:
        """Extract attribute values from elements with a specific tag.
        
        Args:
            file_path: Path to the XML file
            tag_name: XML tag name to search for
            attribute_name: Attribute name to extract
            
        Returns:
            List of attribute values found
        """
        elements = self.extract_elements_by_tag(file_path, tag_name)
        return [
            element.attributes.get(attribute_name, "")
            for element in elements
            if attribute_name in element.attributes
        ]
    
    def get_element_data_as_dict(self, file_path: Union[str, Path]) -> List[Dict[str, str]]:
        """Convert XML elements to list of dictionaries.
        
        This method is useful for compatibility with pandas and other data processing libraries.
        
        Args:
            file_path: Path to the XML file
            
        Returns:
            List of dictionaries, each representing an XML element's children as key-value pairs
        """
        root_element = self.parse_file(file_path)
        result = []
        
        for child in root_element.children:
            element_dict = {}
            for sub_child in child.children:
                if sub_child.text:
                    element_dict[sub_child.tag] = sub_child.text
            if element_dict:
                result.append(element_dict)
                
        return result
    
    def validate_file_structure(self, file_path: Union[str, Path], 
                               expected_root_tag: Optional[str] = None,
                               required_attributes: Optional[List[str]] = None) -> bool:
        """Validate the basic structure of an XML file.
        
        Args:
            file_path: Path to the XML file
            expected_root_tag: Expected root element tag name
            required_attributes: List of required attributes on root element
            
        Returns:
            True if validation passes, False otherwise
        """
        try:
            root_element = self.parse_file(file_path)
            
            if expected_root_tag and root_element.tag != expected_root_tag:
                logger.warning(f"Root tag mismatch in {file_path}: expected '{expected_root_tag}', got '{root_element.tag}'")
                return False
                
            if required_attributes:
                missing_attrs = [attr for attr in required_attributes if attr not in root_element.attributes]
                if missing_attrs:
                    logger.warning(f"Missing required attributes in {file_path}: {missing_attrs}")
                    return False
                    
            return True
            
        except (XMLParseError, FileNotFoundError):
            return False
    
    def clear_cache(self) -> None:
        """Clear the XML parsing cache."""
        with self._cache_lock:
            self._cache.clear()
            self._cache_timestamps.clear()
            logger.debug("XML parser cache cleared")
    
    def get_cache_info(self) -> Dict[str, int]:
        """Get information about the current cache state.
        
        Returns:
            Dictionary with cache statistics
        """
        with self._cache_lock:
            return {
                "cache_size": len(self._cache),
                "cache_max_size": self._cache_max_size,
                "cache_enabled": self._cache_enabled
            }
    
    def _convert_element(self, element: ET.Element, file_path: Path, 
                        parent_line: Optional[int] = None) -> XMLElement:
        """Convert an xml.etree.ElementTree.Element to our XMLElement format."""
        children = [
            self._convert_element(child, file_path, parent_line)
            for child in element
        ]
        
        return XMLElement(
            tag=element.tag,
            attributes=dict(element.attrib),
            text=element.text.strip() if element.text else None,
            children=children,
            file_path=file_path,
            line_number=parent_line  # Line numbers not easily available in ET
        )
    
    def _find_elements_by_tag(self, element: XMLElement, tag_name: str) -> List[XMLElement]:
        """Recursively find all elements with a specific tag name."""
        found_elements = []
        
        if element.tag == tag_name:
            found_elements.append(element)
            
        for child in element.children:
            found_elements.extend(self._find_elements_by_tag(child, tag_name))
            
        return found_elements
    
    def _get_from_cache(self, file_path: Path) -> Optional[XMLElement]:
        """Get parsed XML from cache if available and fresh."""
        with self._cache_lock:
            if file_path not in self._cache:
                return None
                
            # Check if file has been modified since caching
            try:
                file_mtime = file_path.stat().st_mtime
                cached_time = self._cache_timestamps.get(file_path, 0)
                
                if file_mtime > cached_time:
                    # File was modified, remove from cache
                    del self._cache[file_path]
                    del self._cache_timestamps[file_path]
                    return None
                    
                return self._cache[file_path]
                
            except OSError:
                # File no longer exists, remove from cache
                if file_path in self._cache:
                    del self._cache[file_path]
                if file_path in self._cache_timestamps:
                    del self._cache_timestamps[file_path]
                return None
    
    def _add_to_cache(self, file_path: Path, element: XMLElement) -> None:
        """Add parsed XML to cache, managing cache size."""
        with self._cache_lock:
            # If cache is full, remove oldest entry
            if len(self._cache) >= self._cache_max_size:
                oldest_path = min(self._cache_timestamps.items(), key=lambda x: x[1])[0]
                del self._cache[oldest_path]
                del self._cache_timestamps[oldest_path]
            
            self._cache[file_path] = element
            self._cache_timestamps[file_path] = time.time()