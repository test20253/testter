"""Analyzer for checking .gitignore file presence and content.

This module provides analysis capabilities for validating that a .gitignore file
exists and contains the necessary entries for a Python automation framework project.
"""

from typing import List, Dict, Any, Tuple, Set
from pathlib import Path
import logging

from .base_analyzer import BaseAnalyzer, AnalyzerContext

logger = logging.getLogger(__name__)


class GitignoreAnalyzer(BaseAnalyzer):
    """Analyzer for validating .gitignore file configuration.
    
    This analyzer ensures that:
    1. A .gitignore file exists in the repository root
    2. The .gitignore contains critical Python project entries
    3. The .gitignore contains automation framework specific exclusions
    """
    
    # Critical entries that must be present for a Python automation framework
    CRITICAL_ENTRIES = {
        # Python bytecode - essential for any Python project
        '__pycache__/',
        '*.pyc',
        
        # Virtual environments - critical for Python development
        'venv/',
        'env/',
        '.env',
        
        # IDE files - prevent IDE-specific files from being committed
        '.vscode/',
        '.idea/',
        
        # OS files - prevent OS-specific files
        '.DS_Store',
        
        # Logs - prevent log files from being committed
        '*.log',
    }
    
    # Recommended entries for automation frameworks
    RECOMMENDED_ENTRIES = {
        # Additional Python patterns
        '*.py[cod]',
        '*$py.class',
        '.venv/',
        'venv*',
        
        # Testing
        '.pytest_cache/',
        '.coverage',
        'htmlcov/',
        '.tox/',
        
        # Distribution / packaging
        'build/',
        'dist/',
        '*.egg-info/',
        
        # OS files
        'Thumbs.db',
        
        # Temporary files
        '*.tmp',
        '*.temp',
        
        # Backup files
        '*.bak',
        '*~',
        
        # Reports and output
        'reports/',
        'test-results/',
        'screenshots/',
        
        # Local configuration
        'local.properties',
        '.local',
        
        # Node.js (if used for tooling)
        'node_modules/',
        
        # Database files
        '*.db',
        '*.sqlite',
        '*.sqlite3',
    }
    
    def __init__(self, config):
        """Initialize gitignore analyzer.
        
        Args:
            config: Analysis configuration
        """
        super().__init__(config)
        # Use base_path from config if available, otherwise current directory
        if hasattr(config, 'directories') and hasattr(config.directories, 'base_path'):
            self.repo_root = config.directories.base_path
        else:
            self.repo_root = Path.cwd()
        
    def get_analyzer_name(self) -> str:
        """Get the name of this analyzer."""
        return "Gitignore Validation Analyzer"
    
    def get_description(self) -> str:
        """Get description of this analyzer."""
        return ("Validates that .gitignore file exists and contains critical entries "
                "for Python automation framework projects")
    
    def _perform_analysis(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Perform gitignore analysis.
        
        Args:
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings) found during analysis
        """
        errors = []
        warnings = []
        
        gitignore_path = self.repo_root / '.gitignore'
        
        # Check if .gitignore exists
        if not gitignore_path.exists():
            errors.append(
                "CRITICAL: .gitignore file is missing from repository root. "
                "This file is essential for maintaining a clean repository and "
                "preventing sensitive or temporary files from being tracked."
            )
            return errors, warnings
        
        # Read .gitignore content
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                gitignore_content = f.read()
        except Exception as e:
            errors.append(f"Failed to read .gitignore file: {e}")
            return errors, warnings
        
        # Normalize content for analysis
        gitignore_lines = {
            line.strip() 
            for line in gitignore_content.splitlines() 
            if line.strip() and not line.strip().startswith('#')
        }
        
        context.files_processed = 1
        
        # Check for critical missing entries
        missing_critical = self._check_critical_entries(gitignore_lines)
        if missing_critical:
            errors.extend([
                f"CRITICAL: Missing essential .gitignore entry: {entry}. "
                f"This entry is required for Python automation projects."
                for entry in missing_critical
            ])
        
        # Check for recommended missing entries
        missing_recommended = self._check_recommended_entries(gitignore_lines)
        if missing_recommended:
            warnings.extend([
                f"RECOMMENDED: Consider adding .gitignore entry: {entry}. "
                f"This entry helps maintain a cleaner repository."
                for entry in missing_recommended
            ])
        
        # Additional validation for automation framework
        framework_warnings = self._check_framework_specific_entries(gitignore_lines)
        warnings.extend(framework_warnings)
        
        return errors, warnings
    
    def _check_critical_entries(self, gitignore_lines: Set[str]) -> List[str]:
        """Check for missing critical entries.
        
        Args:
            gitignore_lines: Set of non-comment lines from .gitignore
            
        Returns:
            List of missing critical entries
        """
        missing = []
        
        for entry in self.CRITICAL_ENTRIES:
            # Check if entry or a similar pattern exists
            if not self._entry_covered(entry, gitignore_lines):
                missing.append(entry)
        
        return missing
    
    def _check_recommended_entries(self, gitignore_lines: Set[str]) -> List[str]:
        """Check for missing recommended entries.
        
        Args:
            gitignore_lines: Set of non-comment lines from .gitignore
            
        Returns:
            List of missing recommended entries
        """
        missing = []
        
        for entry in self.RECOMMENDED_ENTRIES:
            if not self._entry_covered(entry, gitignore_lines):
                missing.append(entry)
        
        return missing[:5]  # Limit to 5 warnings to avoid noise
    
    def _check_framework_specific_entries(self, gitignore_lines: Set[str]) -> List[str]:
        """Check for automation framework specific considerations.
        
        Args:
            gitignore_lines: Set of non-comment lines from .gitignore
            
        Returns:
            List of framework-specific warnings
        """
        warnings = []
        
        # Note: Tests/resources/keywords/json/ and Tests/resources/keywords/xml/ 
        # are required paths and should not be suggested for gitignore
        
        # Check for common automation artifacts
        automation_patterns = [
            'Screenshots/',
            'TestResults/',
            'logs/',
            'temp/',
            'output/',
        ]
        
        for pattern in automation_patterns:
            if not self._entry_covered(pattern.lower(), gitignore_lines):
                warnings.append(
                    f"FRAMEWORK: Consider adding '{pattern}' for automation artifacts"
                )
        
        return warnings[:3]  # Limit warnings
    
    def _entry_covered(self, entry: str, gitignore_lines: Set[str]) -> bool:
        """Check if an entry is covered by existing .gitignore patterns.
        
        Args:
            entry: Entry to check
            gitignore_lines: Set of gitignore lines
            
        Returns:
            True if the entry is covered by existing patterns
        """
        # Direct match
        if entry in gitignore_lines:
            return True
        
        # Check for pattern variations
        entry_lower = entry.lower()
        
        # Check if any existing pattern would cover this entry
        for line in gitignore_lines:
            line_lower = line.lower()
            
            # Simple pattern matching
            if entry_lower == line_lower:
                return True
            
            # Check for wildcard patterns
            if '*' in line_lower:
                # For entries like 'venv/' check if 'venv*' covers it
                if entry_lower.endswith('/'):
                    entry_base = entry_lower.rstrip('/')
                    if line_lower == entry_base + '*':
                        return True
                
                # For entries like '__pycache__/' check if broader patterns cover it
                if line_lower.replace('*', '').strip('/') in entry_lower:
                    return True
                if entry_lower.replace('/', '') in line_lower.replace('*', ''):
                    return True
            
            # Check for directory patterns - 'venv*' should cover 'venv/', '.venv/', etc.
            if entry_lower.endswith('/') and line_lower.endswith('*'):
                entry_base = entry_lower.rstrip('/')
                line_base = line_lower.rstrip('*')
                if entry_base.startswith(line_base) or line_base.startswith(entry_base):
                    return True
            
            # Check exact directory matches
            if entry_lower.endswith('/') and line_lower.endswith('/'):
                if entry_lower.rstrip('/') == line_lower.rstrip('/'):
                    return True
        
        return False
    
    def _finalize_analysis(self, context: AnalyzerContext) -> Dict[str, Any]:
        """Finalize analysis and return metadata.
        
        Args:
            context: Analysis context
            
        Returns:
            Dictionary of metadata
        """
        gitignore_path = self.repo_root / '.gitignore'
        
        metadata = {
            'gitignore_exists': gitignore_path.exists(),
            'critical_entries_checked': len(self.CRITICAL_ENTRIES),
            'recommended_entries_checked': len(self.RECOMMENDED_ENTRIES),
        }
        
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                metadata['gitignore_lines'] = len(content.splitlines())
                metadata['gitignore_size_bytes'] = len(content.encode('utf-8'))
            except Exception:
                pass
        
        return metadata