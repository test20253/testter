"""Engagement ID spelling analyzer for static code analysis.

This module analyzes Python files for correct usage of 'engagement_id' parameter
names in function definitions, detecting common misspellings and variations.
"""

import ast
from pathlib import Path
from typing import List, Tuple, Dict, Any
import logging

from .base_analyzer import BaseAnalyzer, AnalyzerContext

logger = logging.getLogger(__name__)


class EngagementAnalyzer(BaseAnalyzer):
    """Analyzer for engagement ID parameter spelling validation.
    
    This analyzer scans Python files in the custom methods directory to identify
    function parameters that are similar to 'engagement_id' but incorrectly spelled.
    Common misspellings include variations in capitalization, missing underscores,
    and abbreviated forms.
    """
    
    # Expected parameter name
    EXPECTED_PARAM = "engagement_id"
    
    # Suspicious parameter patterns that should be 'engagement_id'
    SUSPICIOUS_PATTERNS = [
        "engagementid", "engagementId", "engagment_id", "primary_engagement",
        "eng_id", "engagementID", "engagement", "engid", "eng", "eid"
    ]
    
    def get_analyzer_name(self) -> str:
        """Get the name of this analyzer."""
        return "Engagement ID Spelling"
    
    def get_description(self) -> str:
        """Get description of what this analyzer does."""
        return "Validates that function parameters use correct 'engagement_id' spelling"
    
    def _perform_analysis(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Perform engagement ID spelling analysis.
        
        Args:
            context: Analysis context information
            
        Returns:
            Tuple of (errors, warnings) found during analysis
        """
        errors = []
        warnings = []
        
        # Validate custom methods directory exists
        custom_methods_dir = self.config.directories.custom_methods_dir
        error = self._validate_directory_exists(custom_methods_dir, "custom methods")
        if error:
            errors.append(error)
            return errors, warnings
        
        # Get Python files to analyze
        python_files = self._get_files_to_analyze(custom_methods_dir, "*.py")
        context.total_files = len(python_files)
        
        self.logger.info(f"Analyzing {len(python_files)} Python files for engagement ID spelling")
        
        # Scan each file for suspicious parameter names
        all_findings = []
        for file_path in python_files:
            try:
                findings = self._scan_python_file(file_path)
                all_findings.extend(findings)
                context.files_processed += 1
                
            except Exception as e:
                error_msg = f"Failed to analyze {file_path}: {str(e)}"
                self.logger.error(error_msg)
                errors.append(error_msg)
        
        # Check threshold
        total_invalid = len(all_findings)
        threshold_error = self._check_threshold(
            total_invalid,
            "max_invalid_engagement_params",
            self.config.thresholds.max_invalid_engagement_params,
            "invalid engagement parameter usages"
        )
        
        if threshold_error:
            errors.append(threshold_error)
        
        # Convert findings to error messages
        for finding in all_findings:
            error_msg = (f"Invalid engagement parameter in {finding['file']}, "
                        f"function '{finding['function']}': {finding['suspicious_params']}")
            errors.append(error_msg)
        
        # Add summary information
        if all_findings:
            warnings.append(f"Found {total_invalid} functions with incorrect engagement parameter spelling")
        
        return errors, warnings
    
    def _scan_python_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse a Python file and find functions with incorrect engagement_id usage.
        
        Args:
            file_path: Path to the Python file to analyze
            
        Returns:
            List of findings with file, function, and suspicious parameter information
            
        Raises:
            SyntaxError: If the Python file has syntax errors
            OSError: If the file cannot be read
        """
        findings = []
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                
            # Parse the Python file
            tree = ast.parse(content, filename=str(file_path))
            
        except SyntaxError as e:
            self.logger.warning(f"Syntax error in {file_path}: {e}")
            raise
        except UnicodeDecodeError as e:
            self.logger.warning(f"Encoding error in {file_path}: {e}")
            raise
        
        # Walk through all nodes in the AST
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Get parameter names from function definition
                param_names = [arg.arg for arg in node.args.args]
                
                # Check for suspicious parameter names
                suspicious = [p for p in param_names if self._is_similar_param(p)]
                
                if suspicious:
                    findings.append({
                        "file": str(file_path.relative_to(self.config.directories.base_path)),
                        "function": node.name,
                        "suspicious_params": suspicious
                    })
        
        return findings
    
    def _is_similar_param(self, param_name: str) -> bool:
        """Check if a parameter name is suspicious (similar to but not exactly 'engagement_id').
        
        Args:
            param_name: Parameter name to check
            
        Returns:
            True if the parameter name matches suspicious patterns
        """
        return (param_name.lower() in [p.lower() for p in self.SUSPICIOUS_PATTERNS] 
                and param_name != self.EXPECTED_PARAM)
    
    def _finalize_analysis(self, context: AnalyzerContext) -> Dict[str, Any]:
        """Finalize analysis and return metadata.
        
        Args:
            context: Analysis context information
            
        Returns:
            Dictionary of metadata about the analysis
        """
        return {
            "directory_scanned": str(self.config.directories.custom_methods_dir),
            "expected_parameter": self.EXPECTED_PARAM,
            "suspicious_patterns": self.SUSPICIOUS_PATTERNS,
            "threshold": self.config.thresholds.max_invalid_engagement_params
        }