"""
Diff Module - Implements diff algorithm using dynamic programming

DSA Concepts:
- Dynamic Programming: Longest Common Subsequence (LCS)
- 2D DP Table: For computing LCS
- Backtracking: To reconstruct diff from DP table
"""

from typing import List, Tuple


class DiffLine:
    """Represents a line in the diff output."""
    
    def __init__(self, line_type: str, content: str, line_num: int = 0):
        """
        Initialize diff line.
        
        Args:
            line_type: '+' for addition, '-' for deletion, ' ' for unchanged
            content: Line content
            line_num: Line number in original file
        """
        self.line_type = line_type
        self.content = content
        self.line_num = line_num
    
    def __str__(self) -> str:
        return f"{self.line_type} {self.content}"


def compute_lcs_length(text1: List[str], text2: List[str]) -> List[List[int]]:
    """
    Compute LCS length using dynamic programming.
    
    Time Complexity: O(m * n) where m, n are lengths of texts
    Space Complexity: O(m * n) for DP table
    
    Args:
        text1: First text as list of lines
        text2: Second text as list of lines
        
    Returns:
        2D DP table where dp[i][j] = LCS length of text1[:i] and text2[:j]
    """
    m, n = len(text1), len(text2)
    
    # Initialize DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                # Characters match - extend LCS
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Characters don't match - take max of previous results
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp


def backtrack_diff(
    text1: List[str],
    text2: List[str],
    dp: List[List[int]]
) -> List[DiffLine]:
    """
    Backtrack through DP table to reconstruct diff.
    
    Time Complexity: O(m + n)
    Space Complexity: O(m + n) for result
    
    Args:
        text1: Original text
        text2: Modified text
        dp: DP table from LCS computation
        
    Returns:
        List of diff lines
    """
    diff = []
    i, j = len(text1), len(text2)
    
    # Backtrack through DP table
    while i > 0 or j > 0:
        if i > 0 and j > 0 and text1[i - 1] == text2[j - 1]:
            # Lines match - unchanged
            diff.append(DiffLine(' ', text1[i - 1], i))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            # Line added in text2
            diff.append(DiffLine('+', text2[j - 1], 0))
            j -= 1
        else:
            # Line deleted from text1
            diff.append(DiffLine('-', text1[i - 1], i))
            i -= 1
    
    # Reverse to get correct order
    diff.reverse()
    return diff


def compute_diff(text1: str, text2: str) -> List[DiffLine]:
    """
    Compute line-by-line diff between two texts using LCS algorithm.
    
    Time Complexity: O(m * n) where m, n are number of lines
    Space Complexity: O(m * n)
    
    Args:
        text1: Original text
        text2: Modified text
        
    Returns:
        List of diff lines
    """
    # Split into lines
    lines1 = text1.splitlines() if text1 else []
    lines2 = text2.splitlines() if text2 else []
    
    # Compute LCS using dynamic programming
    dp = compute_lcs_length(lines1, lines2)
    
    # Backtrack to get diff
    diff = backtrack_diff(lines1, lines2, dp)
    
    return diff


def format_diff(diff: List[DiffLine]) -> str:
    """
    Format diff output for display.
    
    Args:
        diff: List of diff lines
        
    Returns:
        Formatted diff string
    """
    if not diff:
        return "No changes"
    
    lines = []
    for diff_line in diff:
        lines.append(str(diff_line))
    
    return '\n'.join(lines)


def diff_stats(diff: List[DiffLine]) -> Tuple[int, int]:
    """
    Get diff statistics.
    
    Time Complexity: O(n) where n is number of diff lines
    
    Args:
        diff: List of diff lines
        
    Returns:
        Tuple of (additions, deletions)
    """
    additions = sum(1 for line in diff if line.line_type == '+')
    deletions = sum(1 for line in diff if line.line_type == '-')
    return additions, deletions


def has_changes(diff: List[DiffLine]) -> bool:
    """
    Check if diff has any changes.
    
    Time Complexity: O(n)
    
    Args:
        diff: List of diff lines
        
    Returns:
        True if there are additions or deletions
    """
    return any(line.line_type in ['+', '-'] for line in diff)
