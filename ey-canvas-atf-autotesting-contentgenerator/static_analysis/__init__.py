"""Static Analysis Tool for Canvas Automation Test Framework.

This package provides static analysis capabilities for validating Canvas automation
test framework components including XML test cases, API endpoints, and configuration files.

The package follows SOLID principles and clean code practices with a modular design:
- parser/: Parsing and data extraction utilities
- analyzer/: Core analysis and validation logic  
- reporter/: Output and reporting functionality
- utils/: Common utilities and helper functions

Example:
    Basic usage of the static analysis tool:
    
    >>> from static_analysis import run_all_checks
    >>> results = run_all_checks()
    >>> print(f"Found {len(results.errors)} errors")
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import logging

__version__ = "2.0.0"
__author__ = "Canvas Automation Team"

# Configure package-level logging
logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Result of a static analysis check.
    
    Attributes:
        check_name: Name of the analysis check performed
        success: Whether the check passed without errors
        errors: List of error messages found
        warnings: List of warning messages found
        metadata: Additional information about the check
    """
    check_name: str
    success: bool
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]


@dataclass
class AnalysisReport:
    """Complete static analysis report.
    
    Attributes:
        results: List of individual check results
        total_errors: Total number of errors across all checks
        total_warnings: Total number of warnings across all checks
        execution_time: Time taken to run all checks in seconds
    """
    results: List[AnalysisResult]
    total_errors: int
    total_warnings: int
    execution_time: float
    
    @property
    def success(self) -> bool:
        """True if no errors were found in any check."""
        return self.total_errors == 0


# Re-export key classes and functions for easier imports
__all__ = [
    "AnalysisResult",
    "AnalysisReport", 
    "run_all_checks",
    "logger"
]


def run_all_checks() -> AnalysisReport:
    """Run all available static analysis checks.
    
    Returns:
        Complete analysis report with results from all checks.
        
    Raises:
        RuntimeError: If critical analysis components cannot be loaded.
    """
    from .main import run_all_checks as _run_all_checks
    return _run_all_checks()