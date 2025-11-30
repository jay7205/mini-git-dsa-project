"""
Tree Module - Implements tree data structure for directory hierarchy

DSA Concepts:
- N-ary Tree: Each node can have multiple children (files/subdirectories)
- Tree Traversal: DFS for directory structure serialization
"""

from typing import Dict, List, Optional


class TreeNode:
    """
    Node in the directory tree.
    Represents a file or directory with metadata.
    """
    
    def __init__(self, name: str, is_file: bool, content_hash: Optional[str] = None):
        """
        Initialize tree node.
        
        Args:
            name: File or directory name
            is_file: True if file, False if directory
            content_hash: SHA-1 hash of file content (only for files)
        """
        self.name = name
        self.is_file = is_file
        self.content_hash = content_hash  # Only for files
        self.children: Dict[str, TreeNode] = {}  # For directories
    
    def add_child(self, child: 'TreeNode'):
        """
        Add child node.
        
        Time Complexity: O(1)
        
        Args:
            child: Child node to add
        """
        self.children[child.name] = child
    
    def get_child(self, name: str) -> Optional['TreeNode']:
        """
        Get child by name.
        
        Time Complexity: O(1) hash table lookup
        
        Args:
            name: Child name
            
        Returns:
            Child node or None
        """
        return self.children.get(name)
    
    def to_dict(self) -> dict:
        """
        Convert node to dictionary for serialization.
        Uses DFS traversal.
        
        Time Complexity: O(n) where n is number of nodes in subtree
        Space Complexity: O(h) where h is tree height (recursion stack)
        
        Returns:
            Dictionary representation
        """
        result = {
            'name': self.name,
            'is_file': self.is_file,
        }
        
        if self.is_file:
            result['content_hash'] = self.content_hash
        else:
            # Recursively serialize children (DFS)
            result['children'] = {
                name: child.to_dict() 
                for name, child in self.children.items()
            }
        
        return result
    
    @staticmethod
    def from_dict(data: dict) -> 'TreeNode':
        """
        Create node from dictionary.
        Uses DFS traversal for reconstruction.
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(h) where h is tree height
        
        Args:
            data: Dictionary representation
            
        Returns:
            Reconstructed tree node
        """
        node = TreeNode(
            name=data['name'],
            is_file=data['is_file'],
            content_hash=data.get('content_hash')
        )
        
        if not node.is_file:
            # Recursively reconstruct children (DFS)
            for child_data in data.get('children', {}).values():
                child = TreeNode.from_dict(child_data)
                node.add_child(child)
        
        return node


class DirectoryTree:
    """
    Tree structure representing the repository directory hierarchy.
    """
    
    def __init__(self):
        """Initialize directory tree with root."""
        self.root = TreeNode(".", is_file=False)
    
    def add_file(self, path: str, content_hash: str):
        """
        Add file to tree, creating intermediate directories as needed.
        
        Time Complexity: O(d) where d is path depth
        Space Complexity: O(d) for path components
        
        Args:
            path: File path (e.g., "dir/subdir/file.txt")
            content_hash: SHA-1 hash of file content
        """
        parts = path.split('/')
        current = self.root
        
        # Navigate/create directories
        for part in parts[:-1]:
            child = current.get_child(part)
            if child is None:
                child = TreeNode(part, is_file=False)
                current.add_child(child)
            current = child
        
        # Add file
        file_node = TreeNode(parts[-1], is_file=True, content_hash=content_hash)
        current.add_child(file_node)
    
    def get_file_hash(self, path: str) -> Optional[str]:
        """
        Get hash of file at path.
        
        Time Complexity: O(d) where d is path depth
        
        Args:
            path: File path
            
        Returns:
            Content hash or None if not found
        """
        parts = path.split('/')
        current = self.root
        
        for part in parts:
            current = current.get_child(part)
            if current is None:
                return None
        
        return current.content_hash if current.is_file else None
    
    def list_all_files(self) -> List[str]:
        """
        List all files in tree using DFS traversal.
        
        Time Complexity: O(n) where n is total nodes
        Space Complexity: O(h) where h is tree height
        
        Returns:
            List of file paths
        """
        files = []
        
        def dfs(node: TreeNode, path: str):
            """DFS helper function."""
            if node.is_file:
                files.append(path)
            else:
                for child_name, child in node.children.items():
                    child_path = f"{path}/{child_name}" if path else child_name
                    dfs(child, child_path)
        
        dfs(self.root, "")
        return files
    
    def to_dict(self) -> dict:
        """
        Serialize tree to dictionary.
        
        Time Complexity: O(n) where n is total nodes
        
        Returns:
            Dictionary representation
        """
        return self.root.to_dict()
    
    @staticmethod
    def from_dict(data: dict) -> 'DirectoryTree':
        """
        Deserialize tree from dictionary.
        
        Time Complexity: O(n) where n is total nodes
        
        Args:
            data: Dictionary representation
            
        Returns:
            Reconstructed directory tree
        """
        tree = DirectoryTree()
        tree.root = TreeNode.from_dict(data)
        return tree
