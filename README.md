# Mini Git - Version Control System Using Data Structures & Algorithms

A lightweight version control system built from scratch in Python, demonstrating fundamental **Data Structures and Algorithms** concepts.

## 🎯 Project Overview

Mini Git is an educational implementation of a version control system that showcases:
- **Hash Tables** for content-addressable storage
- **N-ary Trees** for directory hierarchy
- **Singly Linked Lists** for commit history
- **Directed Acyclic Graphs (DAG)** for branch management  
- **Dynamic Programming** (LCS algorithm) for file diffs
- **Graph Traversal** for finding common ancestors

## 🏗️ Architecture

```
mini_git/
├── src/
│   ├── hash_object.py       # SHA-1 hashing + hash table storage
│   ├── tree.py              # N-ary tree for directories
│   ├── commit.py            # Linked list for commit history
│   ├── branch.py            # DAG for branch management
│   ├── staging.py           # Hash table for staging area
│   ├── diff.py              # LCS algorithm for diffs
│   ├── merge.py             # Three-way merge algorithm
│   └── repository.py        # Main repository class
├── notebooks/
│   ├── 01_demo_basic_operations.ipynb
│   ├── 02_demo_branching.ipynb
│   └── 03_dsa_analysis.ipynb
├── mini_git.py              # CLI interface
├── README.md
├── DSA_CONCEPTS.md
└── requirements.txt
```

## 📚 DSA Concepts Demonstrated

| Data Structure | Application | Operations |
|----------------|-------------|------------|
| **Hash Table** | File tracking, object storage | O(1) insert/lookup |
| **N-ary Tree** | Directory structure | O(d) add, O(n) traverse |
| **Linked List** | Commit history | O(1) insert, O(n) traverse |
| **DAG** | Branch graph | O(1) create/switch branch |
| **DP (LCS)** | Diff algorithm | O(m×n) time |
| **Graph Traversal** | Common ancestor | O(n+m) time |

## 🚀 Features

- ✅ `init` - Initialize repository
- ✅ `add` - Stage files for commit
- ✅ `commit` - Create commits with messages
- ✅ `log` - View commit history
- ✅ `status` - Check repository status
- ✅ `branch` - Create and list branches
- ✅ `checkout` - Switch between branches
- ✅ `diff` - Show file changes using LCS
- ✅ `merge` - Merge branches with conflict detection

## 📦 Installation

```bash
# Clone or download the project
cd "mini_git"

# No external dependencies required (uses Python standard library)
```

## 💻 Usage

### Initialize Repository
```bash
python mini_git.py init --author "Your Name"
```

### Basic Workflow
```bash
# Create a file
echo "Hello, Mini Git!" > file.txt

# Add file to staging area (Hash Table)
python mini_git.py add file.txt

# Create commit (Linked List node)
python mini_git.py commit -m "Initial commit"

# View history (Linked List traversal)
python mini_git.py log

# Check status
python mini_git.py status
```

### Branching Workflow
```bash
# Create new branch (DAG node)
python mini_git.py branch feature

# Switch to branch (O(1) hash table lookup)
python mini_git.py checkout feature

# Make changes and commit
echo "New feature" > feature.txt
python mini_git.py add feature.txt
python mini_git.py commit -m "Add feature"

# Switch back to main
python mini_git.py checkout main

# Merge (Graph traversal + three-way merge)
python mini_git.py merge feature
```

### View Diff
```bash
# Modify a file
echo "Modified content" >> file.txt

# Show diff (LCS algorithm)
python mini_git.py diff file.txt
```

## 📓 Demonstration Notebooks

1. **`01_demo_basic_operations.ipynb`**
   - Initialize, add, commit operations
   - Hash table efficiency demonstration
   - Tree and linked list visualization

2. **`02_demo_branching.ipynb`**
   - Branch creation and switching
   - DAG visualization
   - Common ancestor finding
   - Merge operations

3. **`03_dsa_analysis.ipynb`**
   - Detailed complexity analysis
   - All algorithms explained with examples
   - Performance benchmarks
   - Complete complexity table

## 🧮 Time Complexity Summary

| Operation | Complexity | Data Structure |
|-----------|------------|----------------|
| Hash file | O(n) | SHA-1 |
| Store/retrieve object | O(1) | Hash table |
| Add file to tree | O(d) | N-ary tree |
| List files | O(n) | DFS traversal |
| Create commit | O(1) | Linked list |
| Get commit history | O(k) | Linked list |
| Create/switch branch | O(1) | Hash table |
| Find common ancestor | O(n+m) | Graph traversal |
| Compute diff | O(m×n) | DP (LCS) |

*Where: n=size, d=depth, k=commits retrieved, m,n=file lines*

## 📖 Documentation

- **[DSA_CONCEPTS.md](DSA_CONCEPTS.md)** - Detailed explanation of all algorithms and data structures
- **Notebooks** - Interactive demonstrations with visualizations
- **Code comments** - Inline complexity analysis

## 🎓 Educational Value

This project demonstrates:
1. **Practical DSA application** - Real-world use of theoretical concepts
2. **Design patterns** - Content-addressable storage, DAG structures
3. **Algorithm selection** - Choosing appropriate algorithms for each operation
4. **Complexity analysis** - Understanding time/space trade-offs

## 🧪 Testing

Run the demonstration notebooks to verify all functionality:

```bash
jupyter notebook notebooks/01_demo_basic_operations.ipynb
jupyter notebook notebooks/02_demo_branching.ipynb
jupyter notebook notebooks/03_dsa_analysis.ipynb
```

## 🔍 Under the Hood

### Content-Addressable Storage
Files are stored by their SHA-1 hash, ensuring:
- Deduplication (same content = same hash)
- Integrity verification
- Efficient storage

### Commit as Linked List Node
```python
Commit {
    tree_hash: str       # Points to directory tree
    parent_hash: str     # Link to parent commit
    message: str
    author: str
    timestamp: datetime
}
```

### Branch as DAG Node
```python
Branch {
    name: str
    commit_hash: str     # Points to commit (graph node)
}
```

## 🛠️ Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)
- Jupyter Notebook (optional, for running demos)

## 📝 License

This is an educational project for DSA demonstration purposes.

## 👨‍💻 Author

Created for DSA in Python course as end-semester project.

## 🙏 Acknowledgments

Inspired by Git's architecture and designed to teach fundamental computer science concepts through practical implementation.

---

**Perfect for**: DSA projects, portfolio demonstrations, learning version control internals, understanding Git architecture
