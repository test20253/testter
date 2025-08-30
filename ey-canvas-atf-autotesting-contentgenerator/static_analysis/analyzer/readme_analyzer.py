"""Analyzer for checking README.md file presence and content.

This module provides analysis capabilities for validating that a README.md file
exists and contains the necessary information for Canvas automation framework projects.
"""

from typing import List, Dict, Any, Tuple, Set, Pattern
from pathlib import Path
import logging
import re

from .base_analyzer import BaseAnalyzer, AnalyzerContext

logger = logging.getLogger(__name__)


class ReadmeAnalyzer(BaseAnalyzer):
    """Analyzer for validating README.md file presence and content.
    
    This analyzer ensures that:
    1. A README.md file exists in the repository root
    2. The README.md contains required sections and information
    3. The README.md includes proper links to contribution guidelines
    4. The README.md has information about tools, versions, and setup
    """
    
    # Required sections that must be present in README
    REQUIRED_SECTIONS = {
        'description': {
            'patterns': [r'#\s*description', r'#.*canvas.*automation', r'description'],
            'description': 'Project description section'
        },
        'features': {
            'patterns': [r'#\s*key\s*features', r'#\s*features', r'functionalities'],
            'description': 'Key features or functionalities section'
        },
        'requirements': {
            'patterns': [r'#\s*requirements', r'#\s*getting\s*started', r'python.*version', r'java.*version'],
            'description': 'Requirements and dependencies section'
        },
        'installation': {
            'patterns': [r'#\s*fresh\s*install', r'#\s*install', r'clone.*repo', r'pip.*install', r'venv'],
            'description': 'Installation instructions section'
        },
        'contribute': {
            'patterns': [r'#\s*contribute', r'#\s*contributing', r'pull.*request'],
            'description': 'Contribution guidelines section'
        }
    }
    
    # Required links that should be present
    REQUIRED_LINKS = {
        'contributing_guidelines': {
            'patterns': [r'contributing.*guidelines', r'CONTRIBUTING\.md'],
            'description': 'Link to CONTRIBUTING.md or Contributing Guidelines'
        },
        'conventional_commits': {
            'patterns': [r'conventional.*commits', r'conventional-commits'],
            'description': 'Link to Conventional Commits documentation'
        },
        'branch_strategy': {
            'patterns': [r'branch.*strategy', r'git.*flow', r'branching.*strategy'],
            'description': 'Link to Branch Strategy and git Flow documentation'
        }
    }
    
    # Required technical information
    REQUIRED_INFO = {
        'python_version': {
            'patterns': [r'python.*version.*\d+\.\d+', r'python.*\d+\.\d+'],
            'description': 'Python version specification'
        },
        'framework_info': {
            'patterns': [r'scriptless', r'robot.*framework', r'selenium'],
            'description': 'Information about automation framework used'
        },
        'execution_info': {
            'patterns': [r'execution', r'run.*test', r'execute.*test', r'test.*script'],
            'description': 'Test execution instructions'
        }
    }
    
    def __init__(self, config):
        """Initialize README analyzer.
        
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
        return "README Documentation Analyzer"
    
    def get_description(self) -> str:
        """Get description of this analyzer."""
        return ("Validates that README.md file exists and contains required information "
                "for Canvas automation framework projects")
    
    def _perform_analysis(self, context: AnalyzerContext) -> Tuple[List[str], List[str]]:
        """Perform README analysis.
        
        Args:
            context: Analysis context
            
        Returns:
            Tuple of (errors, warnings) found during analysis
        """
        errors = []
        warnings = []
        
        readme_path = self.repo_root / 'README.md'
        
        # Check if README.md exists
        if not readme_path.exists():
            errors.append(
                "CRITICAL: README.md file is missing from repository root. "
                "This file is essential for documenting the project, its purpose, "
                "installation steps, and usage instructions."
            )
            return errors, warnings
        
        # Read README.md content
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
        except Exception as e:
            errors.append(f"Failed to read README.md file: {e}")
            return errors, warnings
        
        # Basic validation
        if len(readme_content.strip()) < 100:
            errors.append(
                "CRITICAL: README.md file is too short (less than 100 characters). "
                "The README should contain comprehensive project documentation."
            )
            return errors, warnings
        
        context.files_processed = 1
        
        # Convert content to lowercase for pattern matching
        content_lower = readme_content.lower()
        
        # Check for required sections
        missing_sections = self._check_required_sections(content_lower)
        if missing_sections:
            for section in missing_sections:
                errors.append(
                    f"MISSING SECTION: README.md lacks required '{section['name']}' section. "
                    f"This section should contain: {section['description']}"
                )
        
        # Check for required links
        missing_links = self._check_required_links(readme_content)
        if missing_links:
            for link in missing_links:
                warnings.append(
                    f"MISSING LINK: README.md should include {link['description']}. "
                    f"This helps contributors understand project guidelines."
                )
        
        # Check for required technical information
        missing_info = self._check_required_info(content_lower)
        if missing_info:
            for info in missing_info:
                warnings.append(
                    f"MISSING INFO: README.md should specify {info['description']}. "
                    f"This helps users understand technical requirements."
                )
        
        # Additional structural checks
        structure_warnings = self._check_structure(readme_content)
        warnings.extend(structure_warnings)
        
        return errors, warnings
    
    def _check_required_sections(self, content_lower: str) -> List[Dict[str, str]]:
        """Check for missing required sections.
        
        Args:
            content_lower: README content in lowercase
            
        Returns:
            List of missing sections with metadata
        """
        missing = []
        
        for section_name, section_config in self.REQUIRED_SECTIONS.items():
            section_found = False
            
            for pattern in section_config['patterns']:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    section_found = True
                    break
            
            if not section_found:
                missing.append({
                    'name': section_name,
                    'description': section_config['description']
                })
        
        return missing
    
    def _check_required_links(self, content: str) -> List[Dict[str, str]]:
        """Check for missing required links.
        
        Args:
            content: Original README content (case-sensitive for URLs)
            
        Returns:
            List of missing links with metadata
        """
        missing = []
        
        for link_name, link_config in self.REQUIRED_LINKS.items():
            link_found = False
            
            for pattern in link_config['patterns']:
                if re.search(pattern, content, re.IGNORECASE):
                    link_found = True
                    break
            
            if not link_found:
                missing.append({
                    'name': link_name,
                    'description': link_config['description']
                })
        
        return missing
    
    def _check_required_info(self, content_lower: str) -> List[Dict[str, str]]:
        """Check for missing required technical information.
        
        Args:
            content_lower: README content in lowercase
            
        Returns:
            List of missing information with metadata
        """
        missing = []
        
        for info_name, info_config in self.REQUIRED_INFO.items():
            info_found = False
            
            for pattern in info_config['patterns']:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    info_found = True
                    break
            
            if not info_found:
                missing.append({
                    'name': info_name,
                    'description': info_config['description']
                })
        
        return missing
    
    def _check_structure(self, content: str) -> List[str]:
        """Check README structure and provide recommendations.
        
        Args:
            content: Original README content
            
        Returns:
            List of structural warnings
        """
        warnings = []
        
        # Check for proper heading structure
        headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        if len(headings) < 3:
            warnings.append(
                "STRUCTURE: README.md should have more section headings for better organization. "
                "Consider adding clear sections for different topics."
            )
        
        # Check for code blocks in installation section
        if 'install' in content.lower():
            if not re.search(r'```|`[^`]+`', content):
                warnings.append(
                    "FORMATTING: Consider using code blocks (```) for installation commands "
                    "to improve readability."
                )
        
        # Check for table of contents in long READMEs
        if len(content.split('\n')) > 50:
            if 'table of contents' not in content.lower() and 'toc' not in content.lower():
                warnings.append(
                    "NAVIGATION: Consider adding a Table of Contents for this long README "
                    "to improve navigation."
                )
        
        # Check for badges or status indicators
        if not re.search(r'\[!\[.*\]\(.*\)\]', content) and not re.search(r'badge', content.lower()):
            warnings.append(
                "ENHANCEMENT: Consider adding status badges (build status, version, etc.) "
                "to provide quick project health indicators."
            )
        
        return warnings[:3]  # Limit to 3 warnings to avoid noise
    
    def _finalize_analysis(self, context: AnalyzerContext) -> Dict[str, Any]:
        """Finalize analysis and return metadata.
        
        Args:
            context: Analysis context
            
        Returns:
            Dictionary of metadata
        """
        readme_path = self.repo_root / 'README.md'
        
        metadata = {
            'readme_exists': readme_path.exists(),
            'required_sections_checked': len(self.REQUIRED_SECTIONS),
            'required_links_checked': len(self.REQUIRED_LINKS),
            'required_info_checked': len(self.REQUIRED_INFO),
        }
        
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                metadata['readme_lines'] = len(content.splitlines())
                metadata['readme_size_bytes'] = len(content.encode('utf-8'))
                metadata['readme_characters'] = len(content)
                metadata['headings_count'] = len(re.findall(r'^#+\s+', content, re.MULTILINE))
                metadata['code_blocks_count'] = len(re.findall(r'```', content))
                metadata['links_count'] = len(re.findall(r'\[.*\]\(.*\)', content))
            except Exception:
                pass
        
        return metadata
