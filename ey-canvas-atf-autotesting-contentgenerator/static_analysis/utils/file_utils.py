"""File utility functions for static analysis.

This module provides common file and directory operations used throughout
the static analysis framework.
"""

from pathlib import Path
from typing import List, Optional, Iterator, Set
import logging
import os
import tempfile
from threading import Lock

logger = logging.getLogger(__name__)


class FileUtils:
    """Utility class for file and directory operations."""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        """Singleton pattern to ensure single instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(FileUtils, cls).__new__(cls)
        return cls._instance
    
    @staticmethod
    def find_files(directory: Path, pattern: str = "*", recursive: bool = True) -> List[Path]:
        """Find files matching a pattern in a directory.
        
        Args:
            directory: Directory to search in
            pattern: Glob pattern to match files
            recursive: Whether to search recursively
            
        Returns:
            List of paths to matching files
        """
        if not directory.exists():
            logger.warning(f"Directory does not exist: {directory}")
            return []
        
        if not directory.is_dir():
            logger.warning(f"Path is not a directory: {directory}")
            return []
        
        try:
            if recursive:
                return list(directory.rglob(pattern))
            else:
                return list(directory.glob(pattern))
        except Exception as e:
            logger.error(f"Error finding files in {directory}: {e}")
            return []
    
    @staticmethod
    def ensure_directory_exists(directory: Path) -> bool:
        """Ensure a directory exists, creating it if necessary.
        
        Args:
            directory: Directory path to ensure exists
            
        Returns:
            True if directory exists or was created successfully
        """
        try:
            directory.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {directory}: {e}")
            return False
    
    @staticmethod
    def get_file_size(file_path: Path) -> Optional[int]:
        """Get the size of a file in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes, or None if file doesn't exist or error occurs
        """
        try:
            return file_path.stat().st_size
        except (OSError, FileNotFoundError):
            return None
    
    @staticmethod
    def get_file_modification_time(file_path: Path) -> Optional[float]:
        """Get the modification time of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Modification time as timestamp, or None if error occurs
        """
        try:
            return file_path.stat().st_mtime
        except (OSError, FileNotFoundError):
            return None
    
    @staticmethod
    def is_file_readable(file_path: Path) -> bool:
        """Check if a file is readable.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file is readable
        """
        try:
            return file_path.exists() and os.access(file_path, os.R_OK)
        except Exception:
            return False
    
    @staticmethod
    def filter_files_by_size(files: List[Path], max_size_mb: float) -> List[Path]:
        """Filter files by maximum size.
        
        Args:
            files: List of file paths to filter
            max_size_mb: Maximum file size in megabytes
            
        Returns:
            List of files that are within the size limit
        """
        max_size_bytes = max_size_mb * 1024 * 1024
        filtered_files = []
        
        for file_path in files:
            size = FileUtils.get_file_size(file_path)
            if size is not None and size <= max_size_bytes:
                filtered_files.append(file_path)
            elif size is not None:
                logger.debug(f"Excluding large file: {file_path} ({size / 1024 / 1024:.1f}MB)")
        
        return filtered_files
    
    @staticmethod
    def filter_files_by_exclusions(files: List[Path], excluded_patterns: List[str],
                                  excluded_dirs: List[str]) -> List[Path]:
        """Filter files by exclusion patterns and directories.
        
        Args:
            files: List of file paths to filter
            excluded_patterns: List of file name patterns to exclude
            excluded_dirs: List of directory names to exclude
            
        Returns:
            List of files that are not excluded
        """
        filtered_files = []
        excluded_dirs_set = set(excluded_dirs)
        
        for file_path in files:
            # Check if file is in an excluded directory
            if any(excluded_dir in file_path.parts for excluded_dir in excluded_dirs_set):
                logger.debug(f"Excluding file in excluded directory: {file_path}")
                continue
            
            # Check if file name matches excluded patterns
            excluded = False
            for pattern in excluded_patterns:
                if file_path.match(pattern):
                    logger.debug(f"Excluding file matching pattern '{pattern}': {file_path}")
                    excluded = True
                    break
            
            if not excluded:
                filtered_files.append(file_path)
        
        return filtered_files
    
    @staticmethod
    def create_temp_file(suffix: str = "", prefix: str = "static_analysis_") -> Path:
        """Create a temporary file.
        
        Args:
            suffix: File suffix (e.g., '.xml')
            prefix: File prefix
            
        Returns:
            Path to the created temporary file
        """
        try:
            fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
            os.close(fd)  # Close the file descriptor
            return Path(temp_path)
        except Exception as e:
            logger.error(f"Failed to create temporary file: {e}")
            raise
    
    @staticmethod
    def safe_read_text(file_path: Path, encoding: str = "utf-8", 
                      fallback_encodings: Optional[List[str]] = None) -> Optional[str]:
        """Safely read text from a file with encoding fallback.
        
        Args:
            file_path: Path to the file to read
            encoding: Primary encoding to try
            fallback_encodings: List of fallback encodings to try if primary fails
            
        Returns:
            File content as string, or None if reading fails
        """
        if fallback_encodings is None:
            fallback_encodings = ["latin1", "cp1252"]
        
        encodings_to_try = [encoding] + fallback_encodings
        
        for enc in encodings_to_try:
            try:
                with open(file_path, "r", encoding=enc) as file:
                    return file.read()
            except UnicodeDecodeError:
                logger.debug(f"Failed to read {file_path} with encoding {enc}")
                continue
            except Exception as e:
                logger.error(f"Failed to read file {file_path}: {e}")
                return None
        
        logger.error(f"Failed to read {file_path} with any encoding: {encodings_to_try}")
        return None
    
    @staticmethod
    def get_relative_path(file_path: Path, base_path: Path) -> Path:
        """Get relative path from base path.
        
        Args:
            file_path: File path to make relative
            base_path: Base path to make relative to
            
        Returns:
            Relative path, or original path if relative path cannot be computed
        """
        try:
            return file_path.relative_to(base_path)
        except ValueError:
            # Paths are not relative to each other
            return file_path
    
    @staticmethod
    def walk_directory_safely(directory: Path, follow_symlinks: bool = False) -> Iterator[Path]:
        """Safely walk a directory tree, handling errors gracefully.
        
        Args:
            directory: Directory to walk
            follow_symlinks: Whether to follow symbolic links
            
        Yields:
            Path objects for each file found
        """
        try:
            for root, dirs, files in os.walk(directory, followlinks=follow_symlinks):
                root_path = Path(root)
                
                # Yield files in this directory
                for file_name in files:
                    try:
                        yield root_path / file_name
                    except Exception as e:
                        logger.warning(f"Error processing file {file_name} in {root_path}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error walking directory {directory}: {e}")
    
    @staticmethod
    def count_lines_in_file(file_path: Path) -> Optional[int]:
        """Count the number of lines in a text file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Number of lines, or None if error occurs
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                return sum(1 for _ in file)
        except Exception as e:
            logger.debug(f"Failed to count lines in {file_path}: {e}")
            return None