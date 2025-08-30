"""Main entry point for static analysis tool.

This module provides the primary interface for running static analysis
checks on the Canvas automation framework.
"""

import time
import logging
import sys
from typing import List, Optional
from pathlib import Path

from . import AnalysisResult, AnalysisReport
from .config import load_default_config, load_config_from_env, AnalysisConfig
from .analyzer import DuplicateAnalyzer, SkipAnalyzer, ReferenceAnalyzer, VariableAnalyzer, EngagementAnalyzer, GitignoreAnalyzer, LocatorAnalyzer, ReadmeAnalyzer
from .reporter import ConsoleReporter

logger = logging.getLogger(__name__)


def setup_logging(config: AnalysisConfig) -> None:
    """Set up logging configuration.
    
    Args:
        config: Analysis configuration containing logging settings
    """
    log_level = getattr(logging, config.logging.level.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=config.logging.format,
        handlers=[]
    )
    
    # Add console handler if enabled
    if config.logging.console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        formatter = logging.Formatter(config.logging.format)
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)
    
    # Add file handler if enabled
    if config.logging.file_output:
        try:
            file_handler = logging.FileHandler(config.logging.file_path)
            file_handler.setLevel(log_level)
            formatter = logging.Formatter(config.logging.format)
            file_handler.setFormatter(formatter)
            logging.getLogger().addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Failed to set up file logging: {e}")


def create_analyzers(config: AnalysisConfig) -> List:
    """Create analyzer instances based on configuration.
    
    Args:
        config: Analysis configuration
        
    Returns:
        List of analyzer instances
    """
    analyzers = [
        DuplicateAnalyzer(config),
        SkipAnalyzer(config),
        ReferenceAnalyzer(config),
        VariableAnalyzer(config),
        EngagementAnalyzer(config),
        GitignoreAnalyzer(config),
        LocatorAnalyzer(config),
        ReadmeAnalyzer(config)
    ]
    
    return analyzers


def run_all_checks(config: Optional[AnalysisConfig] = None) -> AnalysisReport:
    """Run all available static analysis checks.
    
    Args:
        config: Optional analysis configuration. If None, loads default config.
        
    Returns:
        Complete analysis report with results from all checks
        
    Raises:
        RuntimeError: If critical analysis components cannot be loaded
    """
    if config is None:
        config = load_config_from_env()
    
    # Set up logging
    setup_logging(config)
    
    logger.info("Starting static analysis")
    
    # Create reporter
    reporter = ConsoleReporter()
    
    # Create analyzers
    try:
        analyzers = create_analyzers(config)
    except Exception as e:
        error_msg = f"Failed to create analyzers: {str(e)}"
        logger.error(error_msg)
        reporter.report_error(error_msg, e)
        raise RuntimeError(error_msg)
    
    # Report start
    analyzer_names = [analyzer.get_analyzer_name() for analyzer in analyzers]
    reporter.report_start(analyzer_names)
    
    # Run analysis
    start_time = time.time()
    results = []
    
    for analyzer in analyzers:
        try:
            reporter.report_check_start(analyzer.get_analyzer_name())
            result = analyzer.analyze()
            results.append(result)
            reporter.report_check_result(result)
            
        except Exception as e:
            error_msg = f"Analysis failed for {analyzer.get_analyzer_name()}: {str(e)}"
            logger.error(error_msg)
            
            # Create a failed result
            failed_result = AnalysisResult(
                check_name=analyzer.get_analyzer_name(),
                success=False,
                errors=[error_msg],
                warnings=[],
                metadata={"execution_time": 0.0, "files_processed": 0}
            )
            results.append(failed_result)
            reporter.report_check_result(failed_result)
    
    # Create final report
    execution_time = time.time() - start_time
    total_errors = sum(len(result.errors) for result in results)
    total_warnings = sum(len(result.warnings) for result in results)
    
    report = AnalysisReport(
        results=results,
        total_errors=total_errors,
        total_warnings=total_warnings,
        execution_time=execution_time
    )
    
    # Report final results
    reporter.report_final_results(report)
    
    logger.info(f"Static analysis completed in {execution_time:.2f}s")
    
    return report


def main() -> int:
    """Main entry point for command-line execution.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        # Load configuration
        config = load_config_from_env()
        
        # Run analysis
        report = run_all_checks(config)
        
        # Return appropriate exit code
        return 0 if report.success else 1
        
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
        return 1
    except Exception as e:
        print(f"Critical error during analysis: {e}")
        logger.exception("Critical error during analysis")
        return 1


if __name__ == "__main__":
    sys.exit(main())
