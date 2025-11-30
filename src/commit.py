"""
Commit Module - Implements linked list structure for commit history

DSA Concepts:
- Singly Linked List: Each commit points to its parent
- Node Structure: Commit as a node with data and pointer
"""

from datetime import datetime
from typing import Optional


class Commit:
    """
    Commit node in the history linked list.
    Each commit points to its parent, forming a chain.
    """
    
    def __init__(
        self,
        tree_hash: str,
        parent_hash: Optional[str],
        message: str,
        author: str,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize commit node.
        
        Args:
            tree_hash: Hash of directory tree snapshot
            parent_hash: Hash of parent commit (None for initial commit)
            message: Commit message
            author: Author name
            timestamp: Commit timestamp (defaults to now)
        """
        self.tree_hash = tree_hash
        self.parent_hash = parent_hash  # Pointer to parent node
        self.message = message
        self.author = author
        self.timestamp = timestamp or datetime.now()
        self.hash: Optional[str] = None  # Set after storage
    
    def to_dict(self) -> dict:
        """
        Serialize commit to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'tree_hash': self.tree_hash,
            'parent_hash': self.parent_hash,
            'message': self.message,
            'author': self.author,
            'timestamp': self.timestamp.isoformat(),
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Commit':
        """
        Deserialize commit from dictionary.
        
        Args:
            data: Dictionary representation
            
        Returns:
            Commit object
        """
        return Commit(
            tree_hash=data['tree_hash'],
            parent_hash=data['parent_hash'],
            message=data['message'],
            author=data['author'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )
    
    def __str__(self) -> str:
        """String representation of commit."""
        return (
            f"Commit: {self.hash}\n"
            f"Author: {self.author}\n"
            f"Date: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"\n    {self.message}\n"
        )


class CommitHistory:
    """
    Manages commit history as a linked list.
    Provides traversal and history operations.
    """
    
    def __init__(self, hash_object):
        """
        Initialize commit history.
        
        Args:
            hash_object: HashObject instance for storage
        """
        self.hash_object = hash_object
    
    def create_commit(
        self,
        tree_hash: str,
        parent_hash: Optional[str],
        message: str,
        author: str
    ) -> str:
        """
        Create and store new commit.
        
        Time Complexity: O(1) for creation + O(n) for hashing
        
        Args:
            tree_hash: Hash of tree snapshot
            parent_hash: Hash of parent commit
            message: Commit message
            author: Author name
            
        Returns:
            Hash of created commit
        """
        commit = Commit(tree_hash, parent_hash, message, author)
        commit_hash = self.hash_object.store_object(commit)
        commit.hash = commit_hash
        return commit_hash
    
    def get_commit(self, commit_hash: str) -> Commit:
        """
        Retrieve commit by hash.
        
        Time Complexity: O(1) hash table lookup
        
        Args:
            commit_hash: Commit hash
            
        Returns:
            Commit object
        """
        commit = self.hash_object.retrieve_object(commit_hash)
        commit.hash = commit_hash
        return commit
    
    def get_commit_history(self, commit_hash: str, max_count: Optional[int] = None) -> list:
        """
        Get commit history by traversing linked list.
        Follows parent pointers from head to tail.
        
        Time Complexity: O(n) where n is number of commits
        Space Complexity: O(n) for storing history
        
        Args:
            commit_hash: Starting commit hash (head of list)
            max_count: Maximum commits to retrieve (None for all)
            
        Returns:
            List of commits in reverse chronological order
        """
        history = []
        current_hash = commit_hash
        count = 0
        
        # Traverse linked list following parent pointers
        while current_hash is not None:
            if max_count and count >= max_count:
                break
            
            commit = self.get_commit(current_hash)
            history.append(commit)
            current_hash = commit.parent_hash  # Follow link to parent
            count += 1
        
        return history
    
    def find_common_ancestor(self, commit1_hash: str, commit2_hash: str) -> Optional[str]:
        """
        Find common ancestor of two commits using set intersection.
        
        Time Complexity: O(n + m) where n, m are depths of commits
        Space Complexity: O(n) for storing ancestors
        
        Args:
            commit1_hash: First commit hash
            commit2_hash: Second commit hash
            
        Returns:
            Hash of common ancestor or None
        """
        # Get all ancestors of commit1
        ancestors1 = set()
        current = commit1_hash
        while current:
            ancestors1.add(current)
            commit = self.get_commit(current)
            current = commit.parent_hash
        
        # Traverse commit2 history until we find a common ancestor
        current = commit2_hash
        while current:
            if current in ancestors1:
                return current
            commit = self.get_commit(current)
            current = commit.parent_hash
        
        return None
    
    def get_commit_count(self, commit_hash: str) -> int:
        """
        Count commits in history by traversing linked list.
        
        Time Complexity: O(n) where n is number of commits
        
        Args:
            commit_hash: Head commit hash
            
        Returns:
            Number of commits
        """
        count = 0
        current = commit_hash
        
        while current:
            count += 1
            commit = self.get_commit(current)
            current = commit.parent_hash
        
        return count
