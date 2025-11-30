"""
Merge Module - Implements three-way merge algorithm

DSA Concepts:
- Graph Traversal: Finding common ancestor in commit graph
- String Matching: Line-by-line comparison
- Conflict Detection: Identifying divergent changes
"""

from typing import Optional, Tuple, List
from .diff import compute_diff, DiffLine


class MergeConflict:
    """Represents a merge conflict."""
    
    def __init__(self, file_path: str, base: str, ours: str, theirs: str):
        """
        Initialize merge conflict.
        
        Args:
            file_path: Path to conflicting file
            base: Content from common ancestor
            ours: Content from current branch
            theirs: Content from merging branch
        """
        self.file_path = file_path
        self.base = base
        self.ours = ours
        self.theirs = theirs
    
    def format_conflict(self) -> str:
        """
        Format conflict in git-style conflict markers.
        
        Returns:
            Conflict formatted with conflict markers
        """
        return (
            f"<<<<<<< HEAD\n"
            f"{self.ours}\n"
            f"=======\n"
            f"{self.theirs}\n"
            f">>>>>>>\n"
        )


class MergeResult:
    """Result of a merge operation."""
    
    def __init__(self):
        """Initialize merge result."""
        self.conflicts: List[MergeConflict] = []
        self.merged_files: dict = {}  # path -> merged content
        self.success = True
    
    def add_conflict(self, conflict: MergeConflict):
        """Add conflict to result."""
        self.conflicts.append(conflict)
        self.success = False
    
    def add_merged_file(self, path: str, content: str):
        """Add successfully merged file."""
        self.merged_files[path] = content
    
    def has_conflicts(self) -> bool:
        """Check if merge has conflicts."""
        return len(self.conflicts) > 0


def three_way_merge(base: str, ours: str, theirs: str) -> Tuple[str, bool]:
    """
    Perform three-way merge on file contents.
    
    Algorithm:
    1. If ours == theirs, no conflict
    2. If ours == base, take theirs (they made changes)
    3. If theirs == base, take ours (we made changes)
    4. If all different, conflict
    
    Time Complexity: O(n) for string comparison
    
    Args:
        base: Content from common ancestor
        ours: Content from current branch
        theirs: Content from merging branch
        
    Returns:
        Tuple of (merged_content, has_conflict)
    """
    # Case 1: No changes or same changes
    if ours == theirs:
        return ours, False
    
    # Case 2: Only theirs modified
    if ours == base:
        return theirs, False
    
    # Case 3: Only ours modified
    if theirs == base:
        return ours, False
    
    # Case 4: Both modified differently - conflict
    return "", True


def merge_files(
    file_path: str,
    base_content: Optional[str],
    ours_content: Optional[str],
    theirs_content: Optional[str]
) -> Tuple[Optional[str], Optional[MergeConflict]]:
    """
    Merge a single file using three-way merge.
    
    Time Complexity: O(n) where n is file size
    
    Args:
        file_path: Path to file
        base_content: Content from common ancestor
        ours_content: Content from current branch
        theirs_content: Content from merging branch
        
    Returns:
        Tuple of (merged_content, conflict)
        If no conflict, conflict is None
        If conflict, merged_content is None
    """
    # Handle file additions/deletions
    if base_content is None:
        # File added in one or both branches
        if ours_content is None:
            return theirs_content, None  # Added in theirs
        elif theirs_content is None:
            return ours_content, None  # Added in ours
        elif ours_content == theirs_content:
            return ours_content, None  # Same addition
        else:
            # Different additions - conflict
            conflict = MergeConflict(file_path, "", ours_content, theirs_content)
            return None, conflict
    
    if ours_content is None and theirs_content is None:
        return None, None  # Both deleted
    
    if ours_content is None:
        # Deleted in ours, modified/unchanged in theirs
        if theirs_content == base_content:
            return None, None  # Deleted in ours, unchanged in theirs
        else:
            # Deleted in ours, modified in theirs - conflict
            conflict = MergeConflict(file_path, base_content, "", theirs_content)
            return None, conflict
    
    if theirs_content is None:
        # Deleted in theirs, modified/unchanged in ours
        if ours_content == base_content:
            return None, None  # Deleted in theirs, unchanged in ours
        else:
            # Deleted in theirs, modified in ours - conflict
            conflict = MergeConflict(file_path, base_content, ours_content, "")
            return None, conflict
    
    # Three-way merge
    merged, has_conflict = three_way_merge(base_content, ours_content, theirs_content)
    
    if has_conflict:
        conflict = MergeConflict(file_path, base_content, ours_content, theirs_content)
        return None, conflict
    
    return merged, None


def perform_merge(
    base_files: dict,    # path -> content
    ours_files: dict,    # path -> content
    theirs_files: dict   # path -> content
) -> MergeResult:
    """
    Perform merge of all files.
    
    Time Complexity: O(n * m) where n is number of files, m is average file size
    
    Args:
        base_files: Files from common ancestor
        ours_files: Files from current branch
        theirs_files: Files from merging branch
        
    Returns:
        MergeResult object
    """
    result = MergeResult()
    
    # Get all file paths
    all_paths = set()
    all_paths.update(base_files.keys())
    all_paths.update(ours_files.keys())
    all_paths.update(theirs_files.keys())
    
    # Merge each file
    for path in all_paths:
        base_content = base_files.get(path)
        ours_content = ours_files.get(path)
        theirs_content = theirs_files.get(path)
        
        merged_content, conflict = merge_files(
            path, base_content, ours_content, theirs_content
        )
        
        if conflict:
            result.add_conflict(conflict)
        elif merged_content is not None:
            result.add_merged_file(path, merged_content)
    
    return result
