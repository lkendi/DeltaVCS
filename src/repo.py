#!/usr/bin/env python3
"""Repo initialization module"""
from config import DELTA_DIR, OBJECTS_DIR, REFS_DIR, HEAD_FILE, INDEX_FILE
import json
import os
import shutil
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

        ignore_patterns = Repository._load_ignore_patterns(".")
        index = json.loads(Utils.read_file(INDEX_FILE) or "{}")

        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"File not found: {file}")

            if Repository._is_ignored(file, ignore_patterns):
                print(f"Ignored `{file}` (matches .deltaignore)")
                continue

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

    @staticmethod
    def clone(source_path: str, destination_path: str) -> None:
        """
        Clones a repository while ignoring files specified in `.deltaignore`.

        Args:
            source_path (str): Path to the source repository.
            destination_path (str): Path to the destination directory.

        Raises:
            ValueError: If the source repository does not exist or is invalid.
        """
        if not os.path.exists(source_path) or not os.path.isdir(source_path):
            raise ValueError(
                "Source repository '{}' does not exist or is invalid.".format(
                    source_path)
            )

        source_delta_dir = os.path.join(source_path, DELTA_DIR)
        if not os.path.exists(source_delta_dir):
            raise ValueError(
                f"'{source_path}' is not a valid repository. Missing .delta "
                f"directory."
            )

        if os.path.exists(destination_path):
            raise ValueError(
                f"Destination directory '{destination_path}' already exists."
            )

        ignore_patterns = Repository._load_ignore_patterns(source_path)

        def ignore_function(directory, contents):
            """Exclude files matching `.deltaignore` patterns."""
            relative_dir = os.path.relpath(directory, source_path)
            return [
                item
                for item in contents
                if Repository._is_ignored(
                    os.path.join(relative_dir, item), ignore_patterns
                )
            ]

        print(
            f"Cloning repository from '{source_path}' "
            f"to '{destination_path}'..."
        )
        shutil.copytree(source_path, destination_path, ignore=ignore_function)

        print("Clone completed successfully.")

    @staticmethod
    def _load_ignore_patterns(repo_path: str) -> list:
        """
        Loads ignore patterns from `.deltaignore`.

        Args:
            repo_path (str): Path to the repository.

        Returns:
            list: A list of patterns to ignore.
        """
        ignore_file = os.path.join(repo_path, ".deltaignore")
        if not os.path.exists(ignore_file):
            print("No ignore file found.")
            return []

        with open(ignore_file, "r") as f:
            return [
                line.strip()
                for line in f
                if line.strip() and not line.startswith("#")
            ]

    @staticmethod
    def _is_ignored(file_path: str, ignore_patterns: list) -> bool:
        """
        Checks if a file matches any ignore patterns.

        Args:
            file_path (str): The file path to check.
            ignore_patterns (list): A list of patterns to ignore.

        Returns:
            bool: True if the file is ignored, False otherwise.
        """
        for pattern in ignore_patterns:
            if Utils.matches_pattern(file_path, pattern):
                return True
        return False
