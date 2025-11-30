#!/usr/bin/env python3
"""
Mini Git - Command Line Interface

A lightweight version control system demonstrating DSA concepts.
"""

import argparse
import sys
import os
from src.repository import Repository


def cmd_init(args):
    """Initialize repository."""
    repo = Repository(args.path)
    if repo.init(args.author):
        print(f"Initialized empty Mini Git repository in {repo.minigit_path}")
        return 0
    else:
        print("Repository already exists")
        return 1


def cmd_add(args):
    """Add files to staging area."""
    repo = Repository(args.path)
    try:
        results = repo.add(args.files)
        for file_path, success in results.items():
            if success:
                print(f"Added: {file_path}")
            else:
                print(f"Failed to add: {file_path}")
        return 0
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1


def cmd_commit(args):
    """Create commit."""
    repo = Repository(args.path)
    try:
        commit_hash = repo.commit(args.message)
        if commit_hash:
            print(f"Created commit: {commit_hash[:8]}")
            return 0
        else:
            print("Nothing to commit")
            return 1
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1


def cmd_log(args):
    """View commit history."""
    repo = Repository(args.path)
    try:
        commits = repo.log(args.number)
        if not commits:
            print("No commits yet")
            return 0
        
        for commit in commits:
            print(commit)
            print()
        return 0
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1


def cmd_status(args):
    """Check repository status."""
    repo = Repository(args.path)
    try:
        status = repo.status()
        
        current_branch = repo.branch_manager.get_current_branch()
        print(f"On branch: {current_branch}\n")
        
        # Staged changes
        if status['staged_new'] or status['staged_modified'] or status['staged_deleted']:
            print("Changes to be committed:")
            for path in status['staged_new']:
                print(f"  new file:   {path}")
            for path in status['staged_modified']:
                print(f"  modified:   {path}")
            for path in status['staged_deleted']:
                print(f"  deleted:    {path}")
            print()
        
        # Unstaged changes
        if status['not_staged_modified'] or status['not_staged_deleted']:
            print("Changes not staged for commit:")
            for path in status['not_staged_modified']:
                print(f"  modified:   {path}")
            for path in status['not_staged_deleted']:
                print(f"  deleted:    {path}")
            print()
        
        # Untracked files
        if status['untracked']:
            print("Untracked files:")
            for path in status['untracked']:
                print(f"  {path}")
            print()
        
        if not any(status.values()):
            print("Working directory clean")
        
        return 0
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1


def cmd_branch(args):
    """Branch operations."""
    repo = Repository(args.path)
    try:
        if args.delete:
            # Delete branch
            if repo.branch(args.name, delete=True):
                print(f"Deleted branch: {args.name}")
                return 0
            else:
                print(f"Failed to delete branch: {args.name}")
                return 1
        elif args.name:
            # Create branch
            if repo.branch(args.name):
                print(f"Created branch: {args.name}")
                return 0
            else:
                print(f"Failed to create branch: {args.name}")
                return 1
        else:
            # List branches
            branches = repo.branch()
            current = repo.branch_manager.get_current_branch()
            for branch in branches:
                if branch == current:
                    print(f"* {branch}")
                else:
                    print(f"  {branch}")
            return 0
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1


def cmd_checkout(args):
    """Checkout branch."""
    repo = Repository(args.path)
    try:
        if repo.checkout(args.branch):
            print(f"Switched to branch: {args.branch}")
            return 0
        else:
            print(f"Branch not found: {args.branch}")
            return 1
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1


def cmd_diff(args):
    """Show diff."""
    repo = Repository(args.path)
    try:
        diff = repo.diff(args.file)
        print(diff)
        return 0
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1


def cmd_merge(args):
    """Merge branch."""
    repo = Repository(args.path)
    try:
        result = repo.merge(args.branch)
        if result['success']:
            print(result.get('message', 'Merge successful'))
            if 'files' in result:
                print(f"Merged files: {', '.join(result['files'])}")
            return 0
        else:
            print(f"Merge failed: {result.get('error', 'Unknown error')}")
            if 'conflicts' in result:
                print("Conflicts in:")
                for path in result['conflicts']:
                    print(f"  {path}")
            return 1
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Mini Git - A lightweight version control system'
    )
    parser.add_argument(
        '--path',
        default='.',
        help='Repository path (default: current directory)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # init
    parser_init = subparsers.add_parser('init', help='Initialize repository')
    parser_init.add_argument('--author', default='Unknown', help='Author name')
    parser_init.set_defaults(func=cmd_init)
    
    # add
    parser_add = subparsers.add_parser('add', help='Add files to staging')
    parser_add.add_argument('files', nargs='+', help='Files to add')
    parser_add.set_defaults(func=cmd_add)
    
    # commit
    parser_commit = subparsers.add_parser('commit', help='Create commit')
    parser_commit.add_argument('-m', '--message', required=True, help='Commit message')
    parser_commit.set_defaults(func=cmd_commit)
    
    # log
    parser_log = subparsers.add_parser('log', help='View commit history')
    parser_log.add_argument('-n', '--number', type=int, help='Number of commits')
    parser_log.set_defaults(func=cmd_log)
    
    # status
    parser_status = subparsers.add_parser('status', help='Check status')
    parser_status.set_defaults(func=cmd_status)
    
    # branch
    parser_branch = subparsers.add_parser('branch', help='Branch operations')
    parser_branch.add_argument('name', nargs='?', help='Branch name')
    parser_branch.add_argument('-d', '--delete', action='store_true', help='Delete branch')
    parser_branch.set_defaults(func=cmd_branch)
    
    # checkout
    parser_checkout = subparsers.add_parser('checkout', help='Checkout branch')
    parser_checkout.add_argument('branch', help='Branch name')
    parser_checkout.set_defaults(func=cmd_checkout)
    
    # diff
    parser_diff = subparsers.add_parser('diff', help='Show diff')
    parser_diff.add_argument('file', help='File to diff')
    parser_diff.set_defaults(func=cmd_diff)
    
    # merge
    parser_merge = subparsers.add_parser('merge', help='Merge branch')
    parser_merge.add_argument('branch', help='Branch to merge')
    parser_merge.set_defaults(func=cmd_merge)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
