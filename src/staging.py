"""
Staging Module - Implements staging area using hash table

DSA Concepts:
- Hash Table: Fast O(1) file lookup and storage
- Key-Value Pairs: File path -> content hash mapping
"""

from typing import Dict, Set, Optional
import os


class StagingArea:
    """
    Staging area for tracking changes before commit.
    Uses hash table for efficient file tracking.
    """
    
    def __init__(self):
        """Initialize empty staging area."""
        self.staged_files: Dict[str, str] = {}  # path -> content_hash
    
    def add_file(self, file_path: str, content_hash: str):
        """
        Add file to staging area.
        
        Time Complexity: O(1) hash table insertion
        Space Complexity: O(1)
        
        Args:
            file_path: Path to file
            content_hash: SHA-1 hash of file content
        """
        # Normalize path
        normalized_path = file_path.replace('\\', '/')
        self.staged_files[normalized_path] = content_hash
    
    def remove_file(self, file_path: str):
        """
        Remove file from staging area.
        
        Time Complexity: O(1) hash table deletion
        
        Args:
            file_path: Path to file
        """
        normalized_path = file_path.replace('\\', '/')
        if normalized_path in self.staged_files:
            del self.staged_files[normalized_path]
    
    def get_file_hash(self, file_path: str) -> Optional[str]:
        """
        Get hash of staged file.
        
        Time Complexity: O(1) hash table lookup
        
        Args:
            file_path: Path to file
            
        Returns:
            Content hash or None
        """
        normalized_path = file_path.replace('\\', '/')
        return self.staged_files.get(normalized_path)
    
    def is_staged(self, file_path: str) -> bool:
        """
        Check if file is staged.
        
        Time Complexity: O(1)
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file is staged
        """
        normalized_path = file_path.replace('\\', '/')
        return normalized_path in self.staged_files
    
    def get_staged_files(self) -> Dict[str, str]:
        """
        Get all staged files.
        
        Time Complexity: O(1) reference return
        
        Returns:
            Dictionary of path -> hash mappings
        """
        return self.staged_files.copy()
    
    def clear(self):
        """
        Clear staging area.
        
        Time Complexity: O(1)
        """
        self.staged_files.clear()
    
    def is_empty(self) -> bool:
        """
        Check if staging area is empty.
        
        Time Complexity: O(1)
        
        Returns:
            True if no files are staged
        """
        return len(self.staged_files) == 0
    
    def get_file_count(self) -> int:
        """
        Get number of staged files.
        
        Time Complexity: O(1)
        
        Returns:
            Number of staged files
        """
        return len(self.staged_files)
    
    def to_dict(self) -> dict:
        """
        Serialize staging area to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'staged_files': self.staged_files
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'StagingArea':
        """
        Deserialize staging area from dictionary.
        
        Args:
            data: Dictionary representation
            
        Returns:
            StagingArea object
        """
        staging = StagingArea()
        staging.staged_files = data.get('staged_files', {})
        return staging


class FileStatus:
    """
    Utility class for determining file status.
    Compares working directory, staging area, and last commit.
    """
    
    @staticmethod
    def get_status(
        working_files: Dict[str, str],  # path -> hash
        staged_files: Dict[str, str],   # path -> hash
        committed_files: Dict[str, str]  # path -> hash
    ) -> dict:
        """
        Determine status of all files.
        
        Time Complexity: O(n) where n is total unique files
        Space Complexity: O(n)
        
        Args:
            working_files: Files in working directory
            staged_files: Files in staging area
            committed_files: Files in last commit
            
        Returns:
            Dictionary with categorized files:
            - staged_new: New files staged for commit
            - staged_modified: Modified files staged for commit
            - staged_deleted: Deleted files staged for commit
            - not_staged_modified: Modified files not staged
            - not_staged_deleted: Deleted files not staged
            - untracked: New files not staged
        """
        # Get all unique file paths
        all_paths: Set[str] = set()
        all_paths.update(working_files.keys())
        all_paths.update(staged_files.keys())
        all_paths.update(committed_files.keys())
        
        status = {
            'staged_new': [],
            'staged_modified': [],
            'staged_deleted': [],
            'not_staged_modified': [],
            'not_staged_deleted': [],
            'untracked': []
        }
        
        for path in all_paths:
            working_hash = working_files.get(path)
            staged_hash = staged_files.get(path)
            committed_hash = committed_files.get(path)
            
            # File in staging area
            if staged_hash is not None:
                if committed_hash is None:
                    status['staged_new'].append(path)
                elif staged_hash != committed_hash:
                    status['staged_modified'].append(path)
                
                # Check if working file differs from staged
                if working_hash != staged_hash:
                    if working_hash is None:
                        status['not_staged_deleted'].append(path)
                    else:
                        status['not_staged_modified'].append(path)
            
            # File not in staging area
            else:
                if committed_hash is not None:
                    # File was committed
                    if working_hash is None:
                        status['not_staged_deleted'].append(path)
                    elif working_hash != committed_hash:
                        status['not_staged_modified'].append(path)
                elif working_hash is not None:
                    # New untracked file
                    status['untracked'].append(path)
        
        return status
