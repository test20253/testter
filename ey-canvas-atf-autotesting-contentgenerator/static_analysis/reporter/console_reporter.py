"""Console-based reporter for static analysis results.

This module provides rich console output for static analysis results,
replacing the scattered print statements in the original tools with
a centralized, consistent reporting interface.
"""

from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
from dataclasses import dataclass

from .. import AnalysisResult, AnalysisReport

logger = logging.getLogger(__name__)

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    logger.warning("Rich library not available, falling back to basic console output")


@dataclass
class ReportStyle:
    """Configuration for report styling.
    
    Attributes:
        use_colors: Whether to use colored output
        show_progress: Whether to show progress indicators
        show_summary: Whether to show summary statistics
        show_details: Whether to show detailed error information
        max_errors_per_check: Maximum errors to show per check (0 = all)
    """
    use_colors: bool = True
    show_progress: bool = True
    show_summary: bool = True
    show_details: bool = True
    max_errors_per_check: int = 0


class ConsoleReporter:
    """Console reporter for static analysis results.
    
    This reporter provides formatted console output using the rich library
    when available, falling back to basic text output otherwise.
    """
    
    def __init__(self, style: Optional[ReportStyle] = None):
        """Initialize console reporter.
        
        Args:
            style: Report styling configuration
        """
        self.style = style or ReportStyle()
        self.console = Console() if RICH_AVAILABLE else None
        
    def report_start(self, check_names: List[str]) -> None:
        """Report the start of static analysis.
        
        Args:
            check_names: List of check names that will be performed
        """
        if self.console and self.style.use_colors:
            panel = Panel(
                f"Starting static analysis with {len(check_names)} checks:\n" +
                "\n".join(f"• {name}" for name in check_names),
                title="🔍 Static Analysis",
                border_style="blue"
            )
            self.console.print(panel)
        else:
            print(f"\n--- Static Analysis Starting ---")
            print(f"Running {len(check_names)} checks:")
            for name in check_names:
                print(f"  - {name}")
            print()
    
    def report_check_start(self, check_name: str) -> None:
        """Report the start of an individual check.
        
        Args:
            check_name: Name of the check being started
        """
        if self.console and self.style.use_colors:
            self.console.print(f"[cyan]🔄 Running {check_name}...[/cyan]")
        else:
            print(f"Running {check_name}...")
    
    def report_check_result(self, result: AnalysisResult) -> None:
        """Report the result of an individual check.
        
        Args:
            result: Analysis result to report
        """
        if self.console and self.style.use_colors:
            self._report_check_result_rich(result)
        else:
            self._report_check_result_text(result)
    
    def report_final_results(self, report: AnalysisReport) -> None:
        """Report the final analysis results.
        
        Args:
            report: Complete analysis report
        """
        if self.console and self.style.use_colors:
            self._report_final_results_rich(report)
        else:
            self._report_final_results_text(report)
    
    def report_error(self, message: str, exception: Optional[Exception] = None) -> None:
        """Report an error message.
        
        Args:
            message: Error message
            exception: Optional exception for additional details
        """
        if self.console and self.style.use_colors:
            error_text = f"[bold red]❌ ERROR:[/bold red] {message}"
            if exception and self.style.show_details:
                error_text += f"\n[dim]Details: {str(exception)}[/dim]"
            self.console.print(Panel(error_text, border_style="red"))
        else:
            print(f"\nERROR: {message}")
            if exception and self.style.show_details:
                print(f"Details: {str(exception)}")
    
    def _report_check_result_rich(self, result: AnalysisResult) -> None:
        """Report check result using rich formatting."""
        if result.success:
            self.console.print(f"[green]✅ {result.check_name}: PASSED[/green]")
        else:
            self.console.print(f"[red]❌ {result.check_name}: FAILED[/red]")
            
            if result.errors and self.style.show_details:
                error_table = Table(title=f"Errors in {result.check_name}", header_style="bold red")
                error_table.add_column("Error", style="red", overflow="fold")
                
                errors_to_show = result.errors
                if self.style.max_errors_per_check > 0:
                    errors_to_show = result.errors[:self.style.max_errors_per_check]
                    
                for error in errors_to_show:
                    error_table.add_row(error)
                    
                if len(result.errors) > len(errors_to_show):
                    error_table.add_row(f"... and {len(result.errors) - len(errors_to_show)} more errors")
                
                self.console.print(error_table)
        
        # Show warnings for both passed and failed checks
        if result.warnings and self.style.show_details:
            for warning in result.warnings:
                self.console.print(f"[yellow]⚠️ {warning}[/yellow]")
    
    def _report_check_result_text(self, result: AnalysisResult) -> None:
        """Report check result using plain text formatting."""
        status = "PASSED" if result.success else "FAILED"
        print(f"  {result.check_name}: {status}")
        
        if not result.success and self.style.show_details:
            if result.errors:
                print(f"    Errors ({len(result.errors)}):")
                errors_to_show = result.errors
                if self.style.max_errors_per_check > 0:
                    errors_to_show = result.errors[:self.style.max_errors_per_check]
                    
                for error in errors_to_show:
                    print(f"      - {error}")
                    
                if len(result.errors) > len(errors_to_show):
                    print(f"      ... and {len(result.errors) - len(errors_to_show)} more errors")
        
        # Show warnings for both passed and failed checks
        if result.warnings and self.style.show_details:
            print(f"    Warnings ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"      - {warning}")
    
    def _report_final_results_rich(self, report: AnalysisReport) -> None:
        """Report final results using rich formatting."""
        if not self.style.show_summary:
            return
            
        # Create summary table
        summary_table = Table(title="📊 Analysis Summary", header_style="bold blue")
        summary_table.add_column("Check", style="cyan")
        summary_table.add_column("Status", justify="center")
        summary_table.add_column("Errors", justify="center", style="red")
        summary_table.add_column("Warnings", justify="center", style="yellow")
        summary_table.add_column("Time (s)", justify="right", style="dim")
        
        for result in report.results:
            status = "[green]✅ PASS[/green]" if result.success else "[red]❌ FAIL[/red]"
            execution_time = result.metadata.get("execution_time", 0)
            
            summary_table.add_row(
                result.check_name,
                status,
                str(len(result.errors)),
                str(len(result.warnings)),
                f"{execution_time:.2f}"
            )
        
        self.console.print(summary_table)
        
        # Overall status panel
        if report.success:
            status_panel = Panel(
                f"[bold green]✅ All checks passed![/bold green]\n\n"
                f"📄 Total checks: {len(report.results)}\n"
                f"⏱️ Total time: {report.execution_time:.2f}s",
                title="🎉 Success",
                border_style="green"
            )
        else:
            status_panel = Panel(
                f"[bold red]❌ {report.total_errors} errors found[/bold red]\n\n"
                f"📄 Total checks: {len(report.results)}\n"
                f"🚨 Failed checks: {sum(1 for r in report.results if not r.success)}\n"
                f"⚠️ Total warnings: {report.total_warnings}\n"
                f"⏱️ Total time: {report.execution_time:.2f}s",
                title="💥 Analysis Failed",
                border_style="red"
            )
        
        self.console.print(status_panel)
    
    def _report_final_results_text(self, report: AnalysisReport) -> None:
        """Report final results using plain text formatting."""
        if not self.style.show_summary:
            return
            
        print(f"\n--- Analysis Summary ---")
        print(f"Total checks: {len(report.results)}")
        print(f"Passed: {sum(1 for r in report.results if r.success)}")
        print(f"Failed: {sum(1 for r in report.results if not r.success)}")
        print(f"Total errors: {report.total_errors}")
        print(f"Total warnings: {report.total_warnings}")
        print(f"Execution time: {report.execution_time:.2f}s")
        
        if report.success:
            print("\n✅ All checks passed!")
        else:
            print(f"\n❌ Analysis failed with {report.total_errors} errors")
    
    def create_progress_context(self, total: int, description: str = "Processing..."):
        """Create a progress context for long-running operations.
        
        Args:
            total: Total number of items to process
            description: Description of the operation
            
        Returns:
            Progress context manager (if rich available) or None
        """
        if self.console and self.style.show_progress and RICH_AVAILABLE:
            return Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
                console=self.console
            )
        return None