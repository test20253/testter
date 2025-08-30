"""Base analyzer class providing common functionality for all analyzers.

This module defines the interface and common behavior that all static analysis
analyzers should implement, following the Template Method pattern.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import logging
import time
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class AnalyzerError(Exception):
    """Base exception for analyzer-related errors."""
    pass


@dataclass
class AnalyzerContext:
    """Context information for analysis operations.
    
    Attributes:
        config: Analysis configuration
        start_time: When the analysis started
        files_processed: Number of files processed
        total_files: Total number of files to process
        metadata: Additional context data
    """
    config: Any  # AnalysisConfig - avoiding circular import
    start_time: float
    files_processed: int = 0
    total_files: int = 0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseAnalyzer(ABC):
    """Abstract base class for all static analysis analyzers.
    
    This class provides common functionality and defines the interface
    that all analyzers must implement. It follows the Template Method
    pattern to ensure consistent behavior across analyzers.
    """
    
    def __init__(self, config):
        """Initialize the analyzer with configuration.
        
        Args:
            config: Analysis configuration object
        """
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def analyze(self):
        """Run the analysis and return results.
        
        This is the main entry point for running an analysis. It follows
        the Template Method pattern to ensure consistent behavior.
        
        Returns:
            AnalysisResult containing the analysis findings
            
        Raises:
            AnalyzerError: If analysis fails critically
        """
        from .. import AnalysisResult  # Import here to avoid circular import
        
        start_time = time.time()
        context = AnalyzerContext(
            config=self.config,
            start_time=start_time
        )
        
        self.logger.info(f"Starting {self.get_analyzer_name()} analysis")
        
        try:
            # Template method steps
            self._prepare_analysis(context)
            errors, warnings = self._perform_analysis(context)
            metadata = self._finalize_analysis(context)
            
            execution_time = time.time() - start_time
            success = len(errors) == 0
            
            result = AnalysisResult(
                check_name=self.get_analyzer_name(),
                success=success,
                errors=errors,
                warnings=warnings,
                metadata={
                    "execution_time": execution_time,
                    "files_processed": context.files_processed,
                    **metadata
                }
            )
            
            self.logger.info(
                f"Completed {self.get_analyzer_name()} analysis: "
                f"{len(errors)} errors, {len(warnings)} warnings "
                f"in {execution_time:.2f}s"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            raise AnalyzerError(f"{self.get_analyzer_name()} analysis failed: {str(e)}")
    
    @abstractmethod
    def get_analyzer_name(self) -> str:
        """Get the human-readable name of this analyzer.
        
        Returns:
            Analyzer name for logging and reporting
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get a description of what this analyzer does.
        
        Returns:
            Human-readable description of the analyzer's purpose
        """
        pass
    
    def _prepare_analysis(self, context: AnalyzerContext) -> None:
        """Prepare for analysis (hook for subclasses).
        
        This method is called before the main analysis begins.
        Subclasses can override this to perform setup tasks.
        
        Args:
            context: Analysis context information
        """
        pass
    
    @abstractmethod
    def _perform_analysis(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Perform the core analysis logic.
        
        This method must be implemented by subclasses to perform
        the actual analysis work.
        
        Args:
            context: Analysis context information
            
        Returns:
            Tuple of (errors, warnings) found during analysis
        """
        pass
    
    def _finalize_analysis(self, context: AnalyzerContext) -> Dict[str, Any]:
        """Finalize analysis and return metadata (hook for subclasses).
        
        This method is called after the main analysis completes.
        Subclasses can override this to perform cleanup or generate
        additional metadata.
        
        Args:
            context: Analysis context information
            
        Returns:
            Dictionary of metadata to include in results
        """
        return {}
    
    def _get_files_to_analyze(self, directory: Path, pattern: str = "*.xml") -> List[Path]:
        """Get list of files to analyze in a directory.
        
        Args:
            directory: Directory to scan
            pattern: Glob pattern for file matching
            
        Returns:
            List of files that match the pattern and are not excluded
        """
        if not directory.exists():
            self.logger.warning(f"Directory does not exist: {directory}")
            return []
        
        all_files = list(directory.glob(pattern))
        
        # Filter out excluded files
        filtered_files = []
        for file_path in all_files:
            if self._should_exclude_file(file_path):
                self.logger.debug(f"Excluding file: {file_path}")
                continue
            filtered_files.append(file_path)
        
        return filtered_files
    
    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if a file should be excluded from analysis.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if the file should be excluded
        """
        # Check against excluded files list
        if file_path.name in self.config.excluded_files:
            return True
        
        # Check against excluded directories
        for excluded_dir in self.config.excluded_dirs:
            if excluded_dir in file_path.parts:
                return True
        
        # Check file size if limit is configured
        if hasattr(self.config.thresholds, 'max_file_size_mb'):
            try:
                file_size_mb = file_path.stat().st_size / (1024 * 1024)
                if file_size_mb > self.config.thresholds.max_file_size_mb:
                    self.logger.warning(f"File too large, skipping: {file_path} ({file_size_mb:.1f}MB)")
                    return True
            except OSError:
                self.logger.warning(f"Cannot check file size: {file_path}")
                return True
        
        return False
    
    def _check_threshold(self, actual_count: int, threshold_name: str, 
                        threshold_value: int, item_description: str) -> Optional[str]:
        """Check if a count exceeds a configured threshold.
        
        Args:
            actual_count: Actual count found
            threshold_name: Name of the threshold for logging
            threshold_value: Maximum allowed value
            item_description: Description of what is being counted
            
        Returns:
            Error message if threshold exceeded, None otherwise
        """
        if actual_count > threshold_value:
            return (f"Too many {item_description} found ({actual_count} > {threshold_value}). "
                   f"Threshold: {threshold_name}")
        return None
    
    def _validate_directory_exists(self, directory: Path, description: str) -> Optional[str]:
        """Validate that a required directory exists.
        
        Args:
            directory: Directory path to check
            description: Human-readable description of the directory
            
        Returns:
            Error message if directory missing, None otherwise
        """
        if not directory.exists():
            return f"Required directory does not exist: {directory} ({description})"
        
        if not directory.is_dir():
            return f"Path exists but is not a directory: {directory} ({description})"
        
        return None