"""
Branch Module - Implements branch management using graph structure

DSA Concepts:
- Directed Acyclic Graph (DAG): Branch relationships
- Graph Nodes: Branches as nodes pointing to commits
- Hash Table: Branch name -> commit hash mapping
"""

from typing import Dict, Optional, List


class Branch:
    """
    Represents a branch pointing to a commit.
    """
    
    def __init__(self, name: str, commit_hash: str):
        """
        Initialize branch.
        
        Args:
            name: Branch name
            commit_hash: Hash of commit this branch points to
        """
        self.name = name
        self.commit_hash = commit_hash
    
    def update(self, commit_hash: str):
        """
        Update branch to point to new commit.
        
        Time Complexity: O(1)
        
        Args:
            commit_hash: New commit hash
        """
        self.commit_hash = commit_hash
    
    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            'name': self.name,
            'commit_hash': self.commit_hash
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Branch':
        """Deserialize from dictionary."""
        return Branch(data['name'], data['commit_hash'])


class BranchManager:
    """
    Manages branches in a graph structure.
    Each branch is a node in the graph pointing to a commit.
    The commit history forms a DAG.
    """
    
    def __init__(self):
        """Initialize branch manager."""
        self.branches: Dict[str, Branch] = {}  # Hash table: name -> Branch
        self.current_branch: Optional[str] = None
    
    def create_branch(self, name: str, commit_hash: str) -> bool:
        """
        Create new branch.
        
        Time Complexity: O(1) hash table insertion
        
        Args:
            name: Branch name
            commit_hash: Commit hash to point to
            
        Returns:
            True if created, False if already exists
        """
        if name in self.branches:
            return False
        
        self.branches[name] = Branch(name, commit_hash)
        return True
    
    def delete_branch(self, name: str) -> bool:
        """
        Delete branch.
        
        Time Complexity: O(1) hash table deletion
        
        Args:
            name: Branch name
            
        Returns:
            True if deleted, False if doesn't exist or is current
        """
        if name not in self.branches or name == self.current_branch:
            return False
        
        del self.branches[name]
        return True
    
    def get_branch(self, name: str) -> Optional[Branch]:
        """
        Get branch by name.
        
        Time Complexity: O(1) hash table lookup
        
        Args:
            name: Branch name
            
        Returns:
            Branch object or None
        """
        return self.branches.get(name)
    
    def update_branch(self, name: str, commit_hash: str) -> bool:
        """
        Update branch to point to new commit.
        
        Time Complexity: O(1)
        
        Args:
            name: Branch name
            commit_hash: New commit hash
            
        Returns:
            True if updated, False if doesn't exist
        """
        branch = self.get_branch(name)
        if branch is None:
            return False
        
        branch.update(commit_hash)
        return True
    
    def list_branches(self) -> List[str]:
        """
        List all branch names.
        
        Time Complexity: O(n) where n is number of branches
        
        Returns:
            List of branch names
        """
        return sorted(self.branches.keys())
    
    def switch_branch(self, name: str) -> bool:
        """
        Switch to different branch.
        
        Time Complexity: O(1)
        
        Args:
            name: Branch name
            
        Returns:
            True if switched, False if doesn't exist
        """
        if name not in self.branches:
            return False
        
        self.current_branch = name
        return True
    
    def get_current_branch(self) -> Optional[str]:
        """
        Get current branch name.
        
        Time Complexity: O(1)
        
        Returns:
            Current branch name or None
        """
        return self.current_branch
    
    def get_current_commit(self) -> Optional[str]:
        """
        Get commit hash of current branch.
        
        Time Complexity: O(1)
        
        Returns:
            Commit hash or None
        """
        if self.current_branch is None:
            return None
        
        branch = self.get_branch(self.current_branch)
        return branch.commit_hash if branch else None
    
    def branch_exists(self, name: str) -> bool:
        """
        Check if branch exists.
        
        Time Complexity: O(1)
        
        Args:
            name: Branch name
            
        Returns:
            True if exists
        """
        return name in self.branches
    
    def to_dict(self) -> dict:
        """
        Serialize to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'branches': {
                name: branch.to_dict()
                for name, branch in self.branches.items()
            },
            'current_branch': self.current_branch
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'BranchManager':
        """
        Deserialize from dictionary.
        
        Args:
            data: Dictionary representation
            
        Returns:
            BranchManager object
        """
        manager = BranchManager()
        manager.branches = {
            name: Branch.from_dict(branch_data)
            for name, branch_data in data.get('branches', {}).items()
        }
        manager.current_branch = data.get('current_branch')
        return manager
