"""Reporter modules for static analysis.

This package contains reporting functionality for presenting static analysis
results in various formats and outputs.
"""

from .console_reporter import ConsoleReporter

__all__ = [
    "ConsoleReporter"
]