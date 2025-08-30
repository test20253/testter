"""Analyzer for checking variable definitions in XML files.

This module provides analysis capabilities for checking XML variable files
to ensure they meet the required criteria and format standards.
"""

from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
import logging

from .base_analyzer import BaseAnalyzer, AnalyzerContext
from ..parser.xml_parser import XMLParser, XMLParseError

logger = logging.getLogger(__name__)


class VariableAnalyzer(BaseAnalyzer):
    """Analyzer for checking XML variable definitions.
    
    This analyzer validates XML variable files to ensure they contain
    proper variable definitions with required attributes and values.
    """
    
    def __init__(self, config):
        """Initialize variable analyzer.
        
        Args:
            config: Analysis configuration
        """
        super().__init__(config)
        self.xml_parser = XMLParser()
    
    def get_analyzer_name(self) -> str:
        """Get the name of this analyzer."""
        return "Variable Definition Analyzer"
    
    def get_description(self) -> str:
        """Get description of this analyzer."""
        return ("Validates XML variable definitions to ensure proper format "
                "and checks for empty or missing variable values")
    
    def _perform_analysis(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Perform variable analysis on XML variable files.
        
        Args:
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings) found during analysis
        """
        errors = []
        warnings = []
        
        variables_file = self.config.directories.variables_file
        
        # Validate that the variables file exists
        file_error = self._validate_file_exists(variables_file, "variables file")
        if file_error:
            errors.append(file_error)
            return errors, warnings
        
        try:
            # Analyze the variables file
            file_errors, file_warnings = self._analyze_variables_file(variables_file, context)
            errors.extend(file_errors)
            warnings.extend(file_warnings)
            
            context.files_processed += 1
            
        except Exception as e:
            logger.error(f"Failed to analyze variables file: {e}")
            errors.append(f"Variable analysis failed: {str(e)}")
        
        return errors, warnings
    
    def _analyze_variables_file(self, file_path: Path, 
                               context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Analyze a single variables XML file.
        
        Args:
            file_path: Path to the variables XML file
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings) for this file
        """
        errors = []
        warnings = []
        
        try:
            # Parse the XML file and extract variable elements
            variable_elements = self.xml_parser.extract_elements_by_tag(file_path, "variable")
            
            if not variable_elements:
                warnings.append(f"No variable elements found in {file_path.name}")
                return errors, warnings
            
            non_empty_variables = []
            empty_variables = []
            invalid_variables = []
            
            for variable in variable_elements:
                var_name = variable.attributes.get("name", "")
                var_value = variable.attributes.get("value", "")
                var_vtype = variable.attributes.get("vtype", "")
                
                # Validate variable structure
                if not var_name:
                    invalid_variables.append("Variable with missing 'name' attribute")
                    continue
                
                # Check if variable has non-empty value and vtype
                if var_value and var_value.strip() and var_vtype and var_vtype.strip():
                    non_empty_variables.append({
                        "name": var_name,
                        "value": var_value,
                        "vtype": var_vtype
                    })
                else:
                    empty_variables.append({
                        "name": var_name,
                        "value": var_value,
                        "vtype": var_vtype,
                        "issues": []
                    })
                    
                    # Identify specific issues
                    if not var_value or not var_value.strip():
                        empty_variables[-1]["issues"].append("empty value")
                    if not var_vtype or not var_vtype.strip():
                        empty_variables[-1]["issues"].append("empty vtype")
            
            # Report findings
            if invalid_variables:
                for invalid_var in invalid_variables:
                    errors.append(f"Invalid variable in {file_path.name}: {invalid_var}")
            
            if empty_variables:
                for empty_var in empty_variables:
                    issues = ", ".join(empty_var["issues"])
                    warnings.append(
                        f"Variable '{empty_var['name']}' in {file_path.name} has {issues}"
                    )
            
            # Update context metadata
            context.metadata.update({
                "variables_file_analyzed": str(file_path),
                "total_variables": len(variable_elements),
                "non_empty_variables": len(non_empty_variables),
                "empty_variables": len(empty_variables),
                "invalid_variables": len(invalid_variables)
            })
            
            # Log summary
            logger.info(
                f"Variables analysis: {len(non_empty_variables)} non-empty, "
                f"{len(empty_variables)} empty, {len(invalid_variables)} invalid"
            )
            
        except XMLParseError as e:
            errors.append(f"Failed to parse variables file {file_path.name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error analyzing variables file {file_path}: {e}")
            errors.append(f"Error analyzing variables file {file_path.name}: {str(e)}")
        
        return errors, warnings
    
    def _validate_file_exists(self, file_path: Path, description: str) -> Optional[str]:
        """Validate that a file exists and is readable.
        
        Args:
            file_path: Path to check
            description: Human-readable description of the file
            
        Returns:
            Error message if file missing or invalid, None otherwise
        """
        if not file_path.exists():
            return f"Required file does not exist: {file_path} ({description})"
        
        if not file_path.is_file():
            return f"Path exists but is not a file: {file_path} ({description})"
        
        # Try to check if file is readable
        try:
            with open(file_path, 'r') as f:
                f.read(1)  # Try to read one character
        except PermissionError:
            return f"File exists but is not readable: {file_path} ({description})"
        except Exception as e:
            return f"Error accessing file {file_path} ({description}): {str(e)}"
        
        return None
    
    def _finalize_analysis(self, context: AnalyzerContext) -> Dict[str, Any]:
        """Finalize variable analysis and return metadata.
        
        Args:
            context: Analysis context
            
        Returns:
            Metadata dictionary with analysis summary
        """
        return {
            "total_files_analyzed": context.files_processed,
            "analysis_type": "variable_definitions"
        }