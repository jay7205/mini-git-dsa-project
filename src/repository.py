"""
Repository Module - Main repository management class

Integrates all data structures and provides high-level operations.
"""

import os
import json
from typing import Optional, Dict, List
from .hash_object import HashObject, hash_file
from .tree import DirectoryTree
from .commit import CommitHistory
from .branch import BranchManager
from .staging import StagingArea, FileStatus
from .diff import compute_diff, format_diff
from .merge import perform_merge


class Repository:
    """
    Main repository class integrating all Mini Git components.
    """
    
    MINI_GIT_DIR = '.minigit'
    OBJECTS_DIR = 'objects'
    REFS_DIR = 'refs'
    HEAD_FILE = 'HEAD'
    INDEX_FILE = 'index'
    CONFIG_FILE = 'config'
    
    def __init__(self, root_path: str):
        """
        Initialize repository.
        
        Args:
            root_path: Root directory of repository
        """
        self.root_path = os.path.abspath(root_path)
        self.minigit_path = os.path.join(self.root_path, self.MINI_GIT_DIR)
        self.objects_path = os.path.join(self.minigit_path, self.OBJECTS_DIR)
        self.refs_path = os.path.join(self.minigit_path, self.REFS_DIR)
        self.head_path = os.path.join(self.minigit_path, self.HEAD_FILE)
        self.index_path = os.path.join(self.minigit_path, self.INDEX_FILE)
        self.config_path = os.path.join(self.minigit_path, self.CONFIG_FILE)
        
        # Initialize components if repository exists
        if self.exists():
            self.hash_object = HashObject(self.objects_path)
            self.commit_history = CommitHistory(self.hash_object)
            self.branch_manager = self._load_branches()
            self.staging_area = self._load_staging()
            self.config = self._load_config()
        else:
            self.hash_object = None
            self.commit_history = None
            self.branch_manager = None
            self.staging_area = None
            self.config = {}
    
    def exists(self) -> bool:
        """Check if repository exists."""
        return os.path.exists(self.minigit_path)
    
    def init(self, author: str = "Unknown") -> bool:
        """
        Initialize new repository.
        
        Args:
            author: Default author name
            
        Returns:
            True if initialized, False if already exists
        """
        if self.exists():
            return False
        
        # Create directory structure
        os.makedirs(self.objects_path, exist_ok=True)
        os.makedirs(self.refs_path, exist_ok=True)
        
        # Initialize components
        self.hash_object = HashObject(self.objects_path)
        self.commit_history = CommitHistory(self.hash_object)
        self.branch_manager = BranchManager()
        self.staging_area = StagingArea()
        
        # Create main branch (no commits yet)
        self.branch_manager.create_branch('main', '')
        self.branch_manager.switch_branch('main')
        
        # Save configuration
        self.config = {'author': author}
        self._save_config()
        self._save_branches()
        self._save_staging()
        
        return True
    
    def add(self, file_paths: List[str]) -> Dict[str, bool]:
        """
        Add files to staging area.
        
        Args:
            file_paths: List of file paths to add
            
        Returns:
            Dictionary of path -> success status
        """
        if not self.exists():
            raise RuntimeError("Not a minigit repository")
        
        results = {}
        
        for file_path in file_paths:
            full_path = os.path.join(self.root_path, file_path)
            
            if not os.path.exists(full_path):
                results[file_path] = False
                continue
            
            if os.path.isfile(full_path):
                # Read file content
                with open(full_path, 'rb') as f:
                    content = f.read()
                
                # Store file content and get its hash
                content_hash = self.hash_object.store_object(content)
                
                # Add to staging area
                self.staging_area.add_file(file_path, content_hash)
                results[file_path] = True
            else:
                results[file_path] = False
        
        self._save_staging()
        return results
    
    def commit(self, message: str) -> Optional[str]:
        """
        Create commit with staged changes.
        
        Args:
            message: Commit message
            
        Returns:
            Commit hash or None if nothing to commit
        """
        if not self.exists():
            raise RuntimeError("Not a minigit repository")
        
        if self.staging_area.is_empty():
            return None
        
        # Build tree from staged files
        tree = DirectoryTree()
        for path, content_hash in self.staging_area.get_staged_files().items():
            tree.add_file(path, content_hash)
        
        # Store tree
        tree_hash = self.hash_object.store_object(tree.to_dict())
        
        # Get parent commit
        parent_hash = self.branch_manager.get_current_commit()
        if parent_hash == '':
            parent_hash = None
        
        # Create commit
        author = self.config.get('author', 'Unknown')
        commit_hash = self.commit_history.create_commit(
            tree_hash, parent_hash, message, author
        )
        
        # Update current branch
        current_branch = self.branch_manager.get_current_branch()
        self.branch_manager.update_branch(current_branch, commit_hash)
        
        # Clear staging area
        self.staging_area.clear()
        
        # Save state
        self._save_branches()
        self._save_staging()
        
        return commit_hash
    
    def log(self, max_count: Optional[int] = None) -> List:
        """
        Get commit history.
        
        Args:
            max_count: Maximum commits to retrieve
            
        Returns:
            List of commits
        """
        if not self.exists():
            raise RuntimeError("Not a minigit repository")
        
        current_commit = self.branch_manager.get_current_commit()
        if not current_commit or current_commit == '':
            return []
        
        return self.commit_history.get_commit_history(current_commit, max_count)
    
    def status(self) -> dict:
        """
        Get repository status.
        
        Returns:
            Status dictionary with file categorizations
        """
        if not self.exists():
            raise RuntimeError("Not a minigit repository")
        
        # Get working directory files
        working_files = {}
        for root, dirs, files in os.walk(self.root_path):
            # Skip .minigit directory
            if self.MINI_GIT_DIR in root:
                continue
            
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.root_path)
                rel_path = rel_path.replace('\\', '/')
                
                content_hash = hash_file(full_path)
                working_files[rel_path] = content_hash
        
        # Get committed files
        committed_files = {}
        current_commit = self.branch_manager.get_current_commit()
        if current_commit and current_commit != '':
            commit = self.commit_history.get_commit(current_commit)
            tree_dict = self.hash_object.retrieve_object(commit.tree_hash)
            tree = DirectoryTree.from_dict(tree_dict)
            
            for file_path in tree.list_all_files():
                content_hash = tree.get_file_hash(file_path)
                committed_files[file_path] = content_hash
        
        # Get staged files
        staged_files = self.staging_area.get_staged_files()
        
        # Compute status
        return FileStatus.get_status(working_files, staged_files, committed_files)
    
    def branch(self, branch_name: Optional[str] = None, delete: bool = False) -> any:
        """
        Branch operations.
        
        Args:
            branch_name: Branch name (None to list branches)
            delete: Whether to delete branch
            
        Returns:
            List of branches or success status
        """
        if not self.exists():
            raise RuntimeError("Not a minigit repository")
        
        if branch_name is None:
            # List branches
            return self.branch_manager.list_branches()
        
        if delete:
            # Delete branch
            success = self.branch_manager.delete_branch(branch_name)
            if success:
                self._save_branches()
            return success
        
        # Create branch
        current_commit = self.branch_manager.get_current_commit()
        if current_commit == '':
            current_commit = None
        
        if current_commit is None:
            return False  # Can't create branch without commits
        
        success = self.branch_manager.create_branch(branch_name, current_commit)
        if success:
            self._save_branches()
        
        return success
    
    def checkout(self, branch_name: str) -> bool:
        """
        Checkout branch.
        
        Args:
            branch_name: Branch to checkout
            
        Returns:
            True if successful
        """
        if not self.exists():
            raise RuntimeError("Not a minigit repository")
        
        if not self.branch_manager.branch_exists(branch_name):
            return False
        
        # Switch branch
        success = self.branch_manager.switch_branch(branch_name)
        if success:
            self._save_branches()
            
            # Update working directory (simplified - just clear staging)
            self.staging_area.clear()
            self._save_staging()
        
        return success
    
    def diff(self, file_path: str) -> str:
        """
        Show diff for file.
        
        Args:
            file_path: File to diff
            
        Returns:
            Formatted diff string
        """
        if not self.exists():
            raise RuntimeError("Not a minigit repository")
        
        # Get current file content
        full_path = os.path.join(self.root_path, file_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                current_content = f.read()
        else:
            current_content = ""
        
        # Get committed content
        committed_content = ""
        current_commit = self.branch_manager.get_current_commit()
        if current_commit and current_commit != '':
            commit = self.commit_history.get_commit(current_commit)
            tree_dict = self.hash_object.retrieve_object(commit.tree_hash)
            tree = DirectoryTree.from_dict(tree_dict)
            
            content_hash = tree.get_file_hash(file_path)
            if content_hash:
                committed_bytes = self.hash_object.retrieve_object(content_hash)
                committed_content = committed_bytes.decode('utf-8', errors='ignore')
        
        # Compute diff
        diff = compute_diff(committed_content, current_content)
        return format_diff(diff)
    
    def merge(self, branch_name: str) -> dict:
        """
        Merge branch into current branch.
        
        Args:
            branch_name: Branch to merge
            
        Returns:
            Merge result dictionary
        """
        if not self.exists():
            raise RuntimeError("Not a minigit repository")
        
        if not self.branch_manager.branch_exists(branch_name):
            return {'success': False, 'error': 'Branch does not exist'}
        
        # Get commits
        current_branch = self.branch_manager.get_current_branch()
        current_commit_hash = self.branch_manager.get_current_commit()
        merge_commit_hash = self.branch_manager.get_branch(branch_name).commit_hash
        
        if current_commit_hash == merge_commit_hash:
            return {'success': True, 'message': 'Already up to date'}
        
        # Find common ancestor
        base_commit_hash = self.commit_history.find_common_ancestor(
            current_commit_hash, merge_commit_hash
        )
        
        if base_commit_hash is None:
            return {'success': False, 'error': 'No common ancestor'}
        
        # Get file contents for three-way merge
        base_files = self._get_commit_files(base_commit_hash)
        ours_files = self._get_commit_files(current_commit_hash)
        theirs_files = self._get_commit_files(merge_commit_hash)
        
        # Perform merge
        merge_result = perform_merge(base_files, ours_files, theirs_files)
        
        if merge_result.has_conflicts():
            return {
                'success': False,
                'conflicts': [c.file_path for c in merge_result.conflicts]
            }
        
        # Apply merged files (simplified - just report success)
        return {
            'success': True,
            'message': f'Merged {branch_name} into {current_branch}',
            'files': list(merge_result.merged_files.keys())
        }
    
    def _get_commit_files(self, commit_hash: str) -> Dict[str, str]:
        """Get all files from a commit as path -> content mapping."""
        commit = self.commit_history.get_commit(commit_hash)
        tree_dict = self.hash_object.retrieve_object(commit.tree_hash)
        tree = DirectoryTree.from_dict(tree_dict)
        
        files = {}
        for file_path in tree.list_all_files():
            content_hash = tree.get_file_hash(file_path)
            if content_hash:
                content_bytes = self.hash_object.retrieve_object(content_hash)
                files[file_path] = content_bytes.decode('utf-8', errors='ignore')
        
        return files
    
    def _save_branches(self):
        """Save branch manager state."""
        with open(self.refs_path + '/branches.json', 'w') as f:
            json.dump(self.branch_manager.to_dict(), f, indent=2)
    
    def _load_branches(self) -> BranchManager:
        """Load branch manager state."""
        branches_file = self.refs_path + '/branches.json'
        if os.path.exists(branches_file):
            with open(branches_file, 'r') as f:
                data = json.load(f)
            return BranchManager.from_dict(data)
        return BranchManager()
    
    def _save_staging(self):
        """Save staging area state."""
        with open(self.index_path, 'w') as f:
            json.dump(self.staging_area.to_dict(), f, indent=2)
    
    def _load_staging(self) -> StagingArea:
        """Load staging area state."""
        if os.path.exists(self.index_path):
            with open(self.index_path, 'r') as f:
                data = json.load(f)
            return StagingArea.from_dict(data)
        return StagingArea()
    
    def _save_config(self):
        """Save configuration."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _load_config(self) -> dict:
        """Load configuration."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}
