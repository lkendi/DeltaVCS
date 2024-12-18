#!/usr/bin/env python3
"""Branch module"""
from config import BRANCH_DIR, HEAD_FILE
import os
import re
from utils import Utils


class Branch:
    """Branch class"""

    @staticmethod
    def _validate_branch_name(name: str) -> None:
        """Validates the branch name.

        Args:
            name (str): The name of the branch to validate

        Raises:
            ValueError: If the branch name is invalid
        """
        if not re.match(r"^[a-zA-Z0-9_\-]+$", name):
            raise ValueError(
                "Invalid branch name. Use only letters, numbers, "
                "dashes, and underscores."
            )

    @staticmethod
    def _current_branch() -> str:
        """Returns the name of the current branch."""
        if not os.path.exists(HEAD_FILE):
            raise RuntimeError(
                "HEAD file is missing. Repository might be corrupted."
            )
        head_content = Utils.read_file(HEAD_FILE).strip()
        if head_content.startswith("ref: refs/heads/"):
            return head_content.replace("ref: refs/heads/", "")
        return None

    @staticmethod
    def create(name: str) -> None:
        """
        Creates a new branch.

        Args:
            name (str): The name of the new branch.
        """
        if not Utils.is_repo_initialized():
            raise RuntimeError(
                "Repository not initialized. Run 'delta init' first."
            )
        Branch._validate_branch_name(name)
        os.makedirs(BRANCH_DIR, exist_ok=True)

        branch_path = os.path.join(BRANCH_DIR, name)
        if os.path.exists(branch_path):
            print(f"Branch '{name}' already exists.")
            return

        current_commit = Utils.read_file(HEAD_FILE).strip()
        if current_commit.startswith("ref: refs/heads/"):
            branch_name = current_commit[len("ref: refs/heads/"):].strip()
            ref_path = os.path.join(BRANCH_DIR, branch_name)
            current_commit = Utils.read_file(ref_path).strip()

        if not current_commit:
            print(
                "No commits to base the new branch on. "
                "Create a commit first."
            )
            return

        Utils.write_file(branch_path, current_commit)
        print(f"Created branch '{name}'.")

    @staticmethod
    def delete(name: str) -> None:
        """
        Deletes a branch.

        Args:
            name (str): The name of the branch to delete.
        """
        if not Utils.is_repo_initialized():
            raise RuntimeError(
                "Repository not initialized. Run 'delta init' first."
            )
        Branch._validate_branch_name(name)

        current_branch = Branch._current_branch()
        if name == current_branch:
            print(
                "Cannot delete the current branch. "
                "Switch to another branch first."
            )
            return

        branch_path = os.path.join(BRANCH_DIR, name)
        if not os.path.exists(branch_path):
            print(f"Branch '{name}' does not exist.")
            return

        os.remove(branch_path)
        print(f"Deleted branch '{name}'.")

    @staticmethod
    def list() -> None:
        """
        Lists all branches.
        """
        if not Utils.is_repo_initialized():
            raise RuntimeError(
                "Repository not initialized. Run 'delta init' first."
            )

        branches = os.listdir(BRANCH_DIR)
        if not branches:
            print("No branches found.")
            return

        current_branch = Branch._current_branch()
        print("Branches:")
        for branch in branches:
            if branch == current_branch:
                print(f"* {branch}")
            else:
                print(f"  {branch}")

    @staticmethod
    def switch(name: str) -> None:
        """
        Switches to another branch.

        Args:
            name (str): The name of the branch
            to switch to.
        """
        if not Utils.is_repo_initialized():
            raise RuntimeError(
                "Repository not initialized. Run 'delta init' first."
            )

        Branch._validate_branch_name(name)

        branch_path = os.path.join(BRANCH_DIR, name)
        if not os.path.exists(branch_path):
            print(f"Branch '{name}' does not exist.")
            return

        Utils.write_file(HEAD_FILE, f"ref: refs/heads/{name}")
        print(f"Switched to branch '{name}'.")
