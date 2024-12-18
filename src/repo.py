#!/usr/bin/env python3
"""Repo initialization module"""
from config import DELTA_DIR, OBJECTS_DIR, REFS_DIR, HEAD_FILE, INDEX_FILE
import json
import os
from utils import Utils


class Repository:
    """Repo class"""

    @staticmethod
    def init(path: str = ".") -> bool:
        """
        Initializes a repository.

        If the repository path does not exist, create the necessary
        files and directories for the repository to work.

        Args:
            path (str): Path to the root directory of the repository.
            Defaults to the current directory.

        Returns:
            bool: Whether the repository was successfully initialized.
        """
        repo_path = os.path.join(path, DELTA_DIR)
        if os.path.exists(repo_path):
            print("Repository already initialized.")
            return False

        Utils.create_directory(OBJECTS_DIR)
        Utils.create_directory(REFS_DIR)
        Utils.write_file(HEAD_FILE, "ref: refs/heads/master\n")
        Utils.write_file(INDEX_FILE, "{}")
        print("Initialized an empty repository")
        return True

    @staticmethod
    def add(files: list[str]) -> None:
        """
        Adds files to the staging area.

        Args:
            files (list[str]): List of file paths to add to the staging area.

        Raises:
            FileNotFoundError: If a specified file does not exist.
            RuntimeError: If the repository is not initialized.
        """
        if not Utils.is_repo_initialized():
            raise RuntimeError(
                "Repository not initialized. Run 'delta init' first."
            )

        index = json.loads(Utils.read_file(INDEX_FILE) or "{}")

        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"File not found: {file}")

            file_hash = Utils.compute_hash(file)
            index[file] = file_hash
            print(f"Added `{file}` to staging area.")

        Utils.write_file(INDEX_FILE, json.dumps(index))

    @staticmethod
    def status() -> None:
        """
        Prints the contents of the staging area.

        The output is a list of files with their hashes.
        """
        if not Utils.is_repo_initialized():
            raise RuntimeError(
                "Repository not initialized. Run 'delta init' first."
            )
        index = json.loads(Utils.read_file(INDEX_FILE) or "{}")

        print("Staging area:")
        for file, file_hash in index.items():
            print(f"  {file}: {file_hash}")
