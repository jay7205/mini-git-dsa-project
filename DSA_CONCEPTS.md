# Data Structures and Algorithms in Mini Git

This document provides an in-depth explanation of all DSA concepts used in Mini Git.

## Table of Contents
1. [Hash Tables](#1-hash-tables)
2. [N-ary Trees](#2-n-ary-trees)
3. [Singly Linked Lists](#3-singly-linked-lists)
4. [Directed Acyclic Graphs](#4-directed-acyclic-graphs-dag)
5. [Dynamic Programming - LCS](#5-dynamic-programming---lcs)
6. [Graph Traversal Algorithms](#6-graph-traversal-algorithms)
7. [Complexity Analysis](#7-complexity-analysis)

---

## 1. Hash Tables

### Overview
Hash tables provide O(1) average-case insertion and lookup through hash functions.

### Implementation in Mini Git

#### SHA-1 Hash Function
- **Purpose**: Generate unique identifiers for content
- **Algorithm**: SHA-1 cryptographic hash
- **Output**: 40-character hexadecimal string
- **Property**: Deterministic (same input → same output)

```python
def hash_content(content: bytes) -> str:
    sha1 = hashlib.sha1()
    sha1.update(content)
    return sha1.hexdigest()
```

#### Applications

**1. Object Storage**
- Store objects using their hash as the key
- Content-addressable: same content = same hash = stored once
- Directory structure: `objects/ab/cdef123...` (first 2 chars as subdirectory)

**2. Staging Area**
- File path → content hash mapping
- Fast O(1) lookup to check if file is staged
- Fast O(1) insertion when adding files

**3. Branch Management**
- Branch name → commit hash mapping
- O(1) branch switching and creation

### Complexity Analysis

| Operation | Time | Space | Reasoning |
|-----------|------|-------|-----------|
| Hash computation | O(n) | O(1) | n = content size, iterate through bytes |
| Insert | O(1) avg | O(1) | Hash table insertion |
| Lookup | O(1) avg | O(1) | Hash table lookup |
| Delete | O(1) avg | O(1) | Hash table deletion |

### Why Hash Tables?
- **Fast operations**: Critical for performance with many files
- **Efficient storage**: No duplicate objects stored
- **Integrity**: Hash serves as checksum for corruption detection

---

## 2. N-ary Trees

### Overview
N-ary trees allow each node to have multiple children, perfect for hierarchical structures.

### Implementation in Mini Git

#### Tree Structure
```
TreeNode {
    name: str                    # File or directory name
    is_file: bool               # True if file, False if directory
    content_hash: str           # SHA-1 hash (files only)
    children: Dict[str, TreeNode]  # Hash table of children
}
```

#### Directory Representation
```
root (.)
├── file1.txt (hash: a1b2c3)
├── file2.txt (hash: d4e5f6)
└── src/
    ├── main.py (hash: g7h8i9)
    └── utils/
        └── helper.py (hash: j0k1l2)
```

### Algorithms

#### Add File: O(d)
```python
def add_file(path: str, content_hash: str):
    parts = path.split('/')
    current = root
    
    # Navigate/create directories: O(d) where d = depth
    for part in parts[:-1]:
        child = current.get_child(part)  # O(1) hash lookup
        if child is None:
            child = TreeNode(part, is_file=False)
            current.add_child(child)  # O(1) hash insert
        current = child
    
    # Add file node
    file_node = TreeNode(parts[-1], True, content_hash)
    current.add_child(file_node)
```

#### DFS Traversal: O(n)
```python
def list_all_files() -> List[str]:
    files = []
    
    def dfs(node, path):
        if node.is_file:
            files.append(path)
        else:
            for child_name, child in node.children.items():
                child_path = f"{path}/{child_name}"
                dfs(child, child_path)
    
    dfs(root, "")
    return files
```

### Complexity Analysis

| Operation | Time | Space | Reasoning |
|-----------|------|-------|-----------|
| Add file | O(d) | O(d) | d = path depth, navigate through directories |
| Get file | O(d) | O(1) | Traverse path components |
| List all files | O(n) | O(h) | n = total nodes, h = height (recursion stack) |
| Serialize (DFS) | O(n) | O(h) | Visit all nodes once |

### Why N-ary Trees?
- **Natural hierarchy**: Directories naturally form tree structures
- **Efficient navigation**: O(d) lookup where d is typically small
- **Flexible**: Each directory can have arbitrary number of children
- **Serializable**: Easy to convert to/from dictionary for storage

---

## 3. Singly Linked Lists

### Overview
Each node points to the next node, forming a chain. Perfect for sequential access patterns.

### Implementation in Mini Git

#### Commit as List Node
```python
class Commit:
    tree_hash: str          # Snapshot of directory tree
    parent_hash: str        # Pointer to parent commit (next node)
    message: str
    author: str
    timestamp: datetime
    hash: str              # This node's identifier
```

#### Linked List Structure
```
HEAD (branch pointer)
  ↓
[Commit C3: "Feature X"] parent → hash_of_C2
                                    ↓
                        [Commit C2: "Fix bug"] parent → hash_of_C1
                                                          ↓
                                            [Commit C1: "Initial"] parent → None
```

### Algorithms

#### Create Commit: O(1)
```python
def create_commit(tree_hash, parent_hash, message, author):
    commit = Commit(tree_hash, parent_hash, message, author)
    commit_hash = hash_object.store_object(commit)  # O(1)
    
    # Update branch to point to new commit (new head)
    branch.commit_hash = commit_hash  # O(1)
    
    return commit_hash
```

#### Get History: O(k)
```python
def get_commit_history(commit_hash, max_count):
    history = []
    current_hash = commit_hash
    count = 0
    
    # Traverse linked list following parent pointers
    while current_hash and count < max_count:
        commit = retrieve_object(current_hash)  # O(1) hash lookup
        history.append(commit)
        current_hash = commit.parent_hash  # Follow link
        count += 1
    
    return history  # Total: O(k) where k = commits retrieved
```

### Complexity Analysis

| Operation | Time | Space | Reasoning |
|-----------|------|-------|-----------|
| Create commit | O(1) | O(1) | Add new head node |
| Get history | O(k) | O(k) | k = commits to retrieve, traverse k nodes |
| Count commits | O(n) | O(1) | n = total commits, traverse entire list |
| Find commit | O(n) | O(1) | Worst case: traverse entire list |

### Why Linked Lists?
- **Sequential history**: Git history is naturally sequential
- **Efficient insertion**: Adding new commits is O(1) at head
- **Parent relationship**: Each commit naturally points to its parent
- **DAG compatible**: Can have multiple children pointing to same parent

---

## 4. Directed Acyclic Graphs (DAG)

### Overview
Directed edges with no cycles, perfect for representing version histories and dependencies.

### Implementation in Mini Git

#### Graph Structure
```
Nodes: Commits
Edges: Parent-child relationships (directed)

       main        feature
         ↓            ↓
      [Commit 5]  [Commit 4]
            \        /
             \      /
              \    /
            [Commit 3] ← common ancestor
                 |
            [Commit 2]
                 |
            [Commit 1] ← root
```

#### Branch as Graph Pointer
```python
class Branch:
    name: str
    commit_hash: str  # Points to a node in the commit graph
```

### Algorithms

#### Common Ancestor: O(n + m)
```python
def find_common_ancestor(commit1_hash, commit2_hash):
    # Get all ancestors of commit1: O(n)
    ancestors1 = set()
    current = commit1_hash
    while current:
        ancestors1.add(current)
        commit = get_commit(current)
        current = commit.parent_hash
    
    # Traverse commit2 until finding common: O(m)
    current = commit2_hash
    while current:
        if current in ancestors1:  # O(1) set lookup
            return current
        commit = get_commit(current)
        current = commit.parent_hash
    
    return None
```

### Properties

**Directed**: Parent → child relationship (can't go backward in time)

**Acyclic**: No cycles (impossible to have circular commit history)

**Multiple parents**: Merge commits have multiple parents (not implemented in basic version)

**Multiple children**: One commit can have multiple branches pointing to it

### Complexity Analysis

| Operation | Time | Space | Reasoning |
|-----------|------|-------|-----------|
| Create branch | O(1) | O(1) | Add node to branch hash table |
| Switch branch | O(1) | O(1) | Update current pointer |
| Find common ancestor | O(n+m) | O(n) | n, m = branch depths; store ancestors |
| List branches | O(b) | O(b) | b = number of branches |

### Why DAG?
- **Version history**: Natural representation of code evolution
- **Branching**: Multiple development paths from same point
- **Merging**: Combine different development paths
- **Acyclic**: Time only moves forward, no paradoxes

---

## 5. Dynamic Programming - LCS

### Overview
Longest Common Subsequence algorithm finds the longest sequence common to two sequences.

### Implementation in Mini Git

#### Problem
Given two files (as sequences of lines), find the longest common subsequence to determine differences.

#### DP Recurrence
```
dp[i][j] = LCS length of lines1[0..i] and lines2[0..j]

Base case:
dp[0][j] = 0 for all j
dp[i][0] = 0 for all i

Recurrence:
if lines1[i-1] == lines2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1  # Extend LCS
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # Take max
```

#### Example

**File 1:**
```
Line 1
Line 2
Line 3
```

**File 2:**
```
Line 1
Modified Line 2
Line 3
Line 4
```

**DP Table:**
```
       ""  L1  ML2  L3  L4
    "" 0   0    0   0   0
    L1 0   1    1   1   1
    L2 0   1    1   1   1
    L3 0   1    1   2   2
```

LCS = ["Line 1", "Line 3"], length = 2

#### Backtracking: O(m + n)
```python
def backtrack_diff(lines1, lines2, dp):
    diff = []
    i, j = len(lines1), len(lines2)
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and lines1[i-1] == lines2[j-1]:
            diff.append((' ', lines1[i-1]))  # Unchanged
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j-1] >= dp[i-1][j]):
            diff.append(('+', lines2[j-1]))  # Addition
            j -= 1
        else:
            diff.append(('-', lines1[i-1]))  # Deletion
            i -= 1
    
    diff.reverse()
    return diff
```

### Complexity Analysis

| Step | Time | Space | Reasoning |
|------|------|-------|-----------|
| Build DP table | O(m×n) | O(m×n) | Fill m×n table |
| Backtrack | O(m+n) | O(m+n) | Traverse at most m+n cells |
| **Total** | **O(m×n)** | **O(m×n)** | m, n = number of lines |

### Why LCS for Diff?
- **Optimal substructure**: LCS has optimal substructure property
- **Accurate diffs**: Finds true minimal differences
- **Line-by-line**: Works naturally with text files
- **Standard algorithm**: Used by many diff tools

---

## 6. Graph Traversal Algorithms

### Depth-First Search (DFS)

#### Applications in Mini Git

**1. Tree Serialization**
```python
def to_dict(node):
    if node.is_file:
        return {'name': node.name, 'hash': node.content_hash}
    else:
        return {
            'name': node.name,
            'children': {
                name: to_dict(child)  # Recursive DFS
                for name, child in node.children.items()
            }
        }
```

**2. List All Files**
```python
def list_files(node, path=""):
    if node.is_file:
        return [path]
    
    files = []
    for child_name, child in node.children.items():
        child_path = f"{path}/{child_name}"
        files.extend(list_files(child, child_path))  # DFS
    
    return files
```

**3. Commit History**
```python
def get_history(commit_hash):
    history = []
    current = commit_hash
    
    while current:  # DFS along parent pointers
        commit = get_commit(current)
        history.append(commit)
        current = commit.parent_hash
    
    return history
```

#### Complexity
- **Time**: O(V + E) where V = vertices (nodes), E = edges
- **Space**: O(h) where h = height (recursion stack)

### Why DFS?
- **Natural for trees**: Recursive structure matches tree structure
- **Space efficient**: O(h) space vs O(w) for BFS where w = width
- **Simple implementation**: Recursive code is clean and readable

---

## 7. Complexity Analysis

### Complete Operation Table

| Operation | Data Structure | Time Complexity | Space Complexity |
|-----------|---------------|-----------------|------------------|
| **Storage Operations** |
| Hash content | SHA-1 | O(n) | O(1) |
| Store object | Hash table | O(1) avg | O(1) |
| Retrieve object | Hash table | O(1) avg | O(1) |
| **Tree Operations** |
| Add file to tree | N-ary tree | O(d) | O(d) |
| Get file from tree | N-ary tree | O(d) | O(1) |
| List all files | DFS | O(n) | O(h) |
| Serialize tree | DFS | O(n) | O(h) |
| **Commit Operations** |
| Create commit | Linked list | O(1) | O(1) |
| Get commit | Hash table | O(1) | O(1) |
| Get history | Linked list traversal | O(k) | O(k) |
| Count commits | Linked list traversal | O(n) | O(1) |
| **Branch Operations** |
| Create branch | Hash table | O(1) | O(1) |
| Delete branch | Hash table | O(1) | O(1) |
| Switch branch | Hash table | O(1) | O(1) |
| List branches | Hash table | O(b) | O(b) |
| Find common ancestor | Graph traversal | O(n+m) | O(n) |
| **Diff and Merge** |
| Compute diff (LCS) | Dynamic programming | O(m×n) | O(m×n) |
| Three-way merge | String comparison | O(p) | O(p) |
| **Status Operations** |
| Get file status | Hash table lookups | O(f) | O(f) |

**Notation:**
- n = content/file size or number of nodes
- d = directory depth in path
- h = height of tree
- k = number of commits to retrieve
- b = number of branches
- m, n = number of lines in files for diff
- p = size of file for merge
- f = number of files for status

### Big-O Classes Used

| Class | Operations | Why Used |
|-------|-----------|----------|
| O(1) | Hash table ops, branch ops | Constant time for frequent operations |
| O(log n) | (Not used) | - |
| O(n) | Tree traversal, list traversal | Linear scan necessary |
| O(n log n) | (Not used) | - |
| O(n²) | Diff algorithm (LCS) | DP table, acceptable for text files |

### Space-Time Tradeoffs

**Hash Tables**
- Space: O(k) storage for k objects
- Time: O(1) average operations
- **Tradeoff**: Extra space for fast operations (worth it!)

**DP for Diff**
- Space: O(m×n) DP table
- Time: O(m×n)
- **Tradeoff**: Space for optimal diff (can be optimized to O(min(m,n)))

**Tree Storage**
- Space: O(n) for n files
- Time: O(d) for operations
- **Tradeoff**: Balanced for typical use cases

---

## Summary

Mini Git demonstrates practical application of fundamental DSA concepts:

1. **Hash Tables**: Provide O(1) operations critical for performance
2. **Trees**: Natural representation of hierarchical data
3. **Linked Lists**: Efficient for sequential access patterns
4. **DAGs**: Model complex relationships without cycles
5. **Dynamic Programming**: Solve optimization problems optimally
6. **Graph Traversal**: Explore connected structures systematically

Each data structure and algorithm was chosen for its **specific strengths** matching the **requirements** of version control operations. The implementation prioritizes **correctness** and **clarity** while maintaining **reasonable performance** for educational purposes.
