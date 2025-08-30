"""Configuration management for static analysis tools.

This module centralizes all configuration values used throughout the static analysis
package, replacing hard-coded values with configurable settings.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any
import os


@dataclass
class DirectoryConfig:
    """Configuration for directory paths used in analysis."""
    
    # Base directories
    base_path: Path = Path(".")
    test_cases_dir: Path = Path("Tests/test_cases")
    app_modules_dir: Path = Path("Tests/app_modules") 
    test_suites_dir: Path = Path("Tests/test_suites")
    api_constants_dir: Path = Path("Tests/resources/constants/api")
    dataset_dir: Path = Path("Tests/resources/dataset")
    variables_file: Path = Path("Tests/resources/variable/var.xml")
    custom_methods_dir: Path = Path("Tests/custom_methods")
    
    def __post_init__(self):
        """Convert relative paths to absolute paths based on base_path."""
        if not self.base_path.is_absolute():
            self.base_path = Path.cwd() / self.base_path
            
        for field_name in ["test_cases_dir", "app_modules_dir", "test_suites_dir", 
                          "api_constants_dir", "dataset_dir", "variables_file", "custom_methods_dir"]:
            current_path = getattr(self, field_name)
            if not current_path.is_absolute():
                setattr(self, field_name, self.base_path / current_path)


@dataclass  
class ThresholdConfig:
    """Configuration for analysis thresholds and limits."""
    
    # Maximum allowed values
    max_duplicate_endpoints: int = 0
    max_duplicate_xml_elements: int = 3
    max_skips_test_cases: int = 0
    max_skips_app_modules: int = 0
    max_skips_test_suites: int = 26
    max_validation_errors: int = 0
    max_validation_not_found: int = 11
    max_invalid_engagement_params: int = 7
    max_direct_locators: int = 0
    
    # File processing limits
    max_file_size_mb: int = 10
    xml_parse_timeout_seconds: int = 30


@dataclass
class LoggingConfig:
    """Configuration for logging behavior."""
    
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    console_output: bool = True
    file_output: bool = False
    file_path: Path = Path("static_analysis.log")


@dataclass
class AnalysisConfig:
    """Master configuration combining all config sections."""
    
    directories: DirectoryConfig
    thresholds: ThresholdConfig
    logging: LoggingConfig
    
    # File patterns and exclusions
    xml_file_patterns: List[str]
    python_file_patterns: List[str]
    excluded_files: List[str]
    excluded_dirs: List[str]
    
    # XML-specific settings
    xml_encoding: str = "utf-8"
    xml_tags_to_check: Dict[str, List[str]] = None
    
    # Dataset file exclusions
    dataset_exclusions: List[str] = None
    
    def __post_init__(self):
        """Set default values for optional fields."""
        if self.xml_file_patterns is None:
            self.xml_file_patterns = ["*.xml"]
            
        if self.python_file_patterns is None:
            self.python_file_patterns = ["*.py"]
            
        if self.excluded_files is None:
            self.excluded_files = []
            
        if self.excluded_dirs is None:
            self.excluded_dirs = [".git", "__pycache__", ".pytest_cache"]
            
        if self.xml_tags_to_check is None:
            self.xml_tags_to_check = {
                "test_cases": ["test-case"],
                "test_suites": ["test-suite"],
                "app_modules": ["app-module"]
            }
            
        if self.dataset_exclusions is None:
            self.dataset_exclusions = [
                "Submit Profile.xml",
                "Complete Independence.xml", 
                "Create Submit and Complete Engagement.xml",
                "API Create and complete Engagement.xml"
            ]


def load_default_config() -> AnalysisConfig:
    """Load default configuration for static analysis.
    
    Returns:
        Default configuration object with standard settings.
    """
    return AnalysisConfig(
        directories=DirectoryConfig(),
        thresholds=ThresholdConfig(),
        logging=LoggingConfig(),
        xml_file_patterns=["*.xml"],
        python_file_patterns=["*.py"],
        excluded_files=[],
        excluded_dirs=[".git", "__pycache__", ".pytest_cache"]
    )


def load_config_from_env() -> AnalysisConfig:
    """Load configuration with environment variable overrides.
    
    Environment variables can override default values using the pattern:
    STATIC_ANALYSIS_<SECTION>_<FIELD> (e.g., STATIC_ANALYSIS_THRESHOLDS_MAX_SKIPS_TEST_SUITES)
    
    Returns:
        Configuration object with environment overrides applied.
    """
    config = load_default_config()
    
    # Override thresholds from environment
    threshold_overrides = {
        "max_duplicate_endpoints": "STATIC_ANALYSIS_THRESHOLDS_MAX_DUPLICATE_ENDPOINTS",
        "max_duplicate_xml_elements": "STATIC_ANALYSIS_THRESHOLDS_MAX_DUPLICATE_XML_ELEMENTS", 
        "max_skips_test_cases": "STATIC_ANALYSIS_THRESHOLDS_MAX_SKIPS_TEST_CASES",
        "max_skips_app_modules": "STATIC_ANALYSIS_THRESHOLDS_MAX_SKIPS_APP_MODULES",
        "max_skips_test_suites": "STATIC_ANALYSIS_THRESHOLDS_MAX_SKIPS_TEST_SUITES",
        "max_validation_errors": "STATIC_ANALYSIS_THRESHOLDS_MAX_VALIDATION_ERRORS",
        "max_validation_not_found": "STATIC_ANALYSIS_THRESHOLDS_MAX_VALIDATION_NOT_FOUND",
        "max_invalid_engagement_params": "STATIC_ANALYSIS_THRESHOLDS_MAX_INVALID_ENGAGEMENT_PARAMS",
        "max_direct_locators": "STATIC_ANALYSIS_THRESHOLDS_MAX_DIRECT_LOCATORS"
    }
    
    for field, env_var in threshold_overrides.items():
        env_value = os.getenv(env_var)
        if env_value is not None:
            try:
                setattr(config.thresholds, field, int(env_value))
            except ValueError:
                pass  # Ignore invalid values, keep default
                
    # Override logging from environment
    log_level = os.getenv("STATIC_ANALYSIS_LOG_LEVEL")
    if log_level:
        config.logging.level = log_level.upper()
        
    return config


# Global config instance (can be overridden by importing modules)
default_config = load_default_config()