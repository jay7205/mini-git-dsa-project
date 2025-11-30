"""
Hash Object Module - Implements SHA-1 hashing and content-addressable storage

DSA Concepts:
- Hash Functions: SHA-1 for unique content identification
- Hash Table: Object storage with O(1) lookup
"""

import hashlib
import os
import pickle
from typing import Any


class HashObject:
    """
    Content-addressable storage using SHA-1 hashing.
    Demonstrates hash function application for unique object identification.
    """
    
    def __init__(self, objects_dir: str):
        """
        Initialize hash object storage.
        
        Args:
            objects_dir: Directory to store hashed objects
        """
        self.objects_dir = objects_dir
        os.makedirs(objects_dir, exist_ok=True)
    
    @staticmethod
    def hash_content(content: bytes) -> str:
        """
        Generate SHA-1 hash of content.
        
        Time Complexity: O(n) where n is content length
        Space Complexity: O(1)
        
        Args:
            content: Bytes to hash
            
        Returns:
            40-character hexadecimal SHA-1 hash
        """
        sha1 = hashlib.sha1()
        sha1.update(content)
        return sha1.hexdigest()
    
    def store_object(self, obj: Any) -> str:
        """
        Store object using content-addressable storage.
        
        Time Complexity: O(n) for hashing + O(1) for storage
        Space Complexity: O(n) where n is object size
        
        Args:
            obj: Object to store (will be pickled)
            
        Returns:
            Hash identifier for the stored object
        """
        # Serialize object
        serialized = pickle.dumps(obj)
        
        # Generate hash
        obj_hash = self.hash_content(serialized)
        
        # Store in subdirectory based on first 2 characters (reduces directory size)
        subdir = os.path.join(self.objects_dir, obj_hash[:2])
        os.makedirs(subdir, exist_ok=True)
        
        obj_path = os.path.join(subdir, obj_hash[2:])
        
        # Write if doesn't exist (content-addressable: same content = same hash)
        if not os.path.exists(obj_path):
            with open(obj_path, 'wb') as f:
                f.write(serialized)
        
        return obj_hash
    
    def retrieve_object(self, obj_hash: str) -> Any:
        """
        Retrieve object by hash.
        
        Time Complexity: O(1) hash table lookup
        Space Complexity: O(n) where n is object size
        
        Args:
            obj_hash: Hash identifier
            
        Returns:
            Deserialized object
            
        Raises:
            FileNotFoundError: If hash not found
        """
        subdir = os.path.join(self.objects_dir, obj_hash[:2])
        obj_path = os.path.join(subdir, obj_hash[2:])
        
        if not os.path.exists(obj_path):
            raise FileNotFoundError(f"Object {obj_hash} not found")
        
        with open(obj_path, 'rb') as f:
            serialized = f.read()
        
        return pickle.loads(serialized)
    
    def object_exists(self, obj_hash: str) -> bool:
        """
        Check if object exists in storage.
        
        Time Complexity: O(1)
        
        Args:
            obj_hash: Hash identifier
            
        Returns:
            True if object exists
        """
        subdir = os.path.join(self.objects_dir, obj_hash[:2])
        obj_path = os.path.join(subdir, obj_hash[2:])
        return os.path.exists(obj_path)


def hash_file(file_path: str) -> str:
    """
    Hash file contents.
    
    Time Complexity: O(n) where n is file size
    
    Args:
        file_path: Path to file
        
    Returns:
        SHA-1 hash of file contents
    """
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()
