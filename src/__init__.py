"""Mini Git - Package initialization."""

from .repository import Repository
from .hash_object import HashObject, hash_file
from .tree import DirectoryTree, TreeNode
from .commit import Commit, CommitHistory
from .branch import Branch, BranchManager
from .staging import StagingArea, FileStatus
from .diff import compute_diff, format_diff
from .merge import perform_merge, MergeResult

__all__ = [
    'Repository',
    'HashObject',
    'hash_file',
    'DirectoryTree',
    'TreeNode',
    'Commit',
    'CommitHistory',
    'Branch',
    'BranchManager',
    'StagingArea',
    'FileStatus',
    'compute_diff',
    'format_diff',
    'perform_merge',
    'MergeResult',
]
