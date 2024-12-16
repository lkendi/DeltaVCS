#!/usr/bin/env python3
"""Repo initialization module"""
from utils import Utils
import os


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
        repo_path = os.path.join(path, ".delta")
        if os.path.exists(repo_path):
            print("Repository already initialized.")
            return False

        Utils.create_directory(f"{repo_path}/objects")
        Utils.write_file(f"{repo_path}/HEAD", "ref: refs/heads/master\n")
        Utils.write_file(f"{repo_path}/index", "{}")
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
        repo_path = ".delta"
        objects_path = os.path.join(repo_path, "objects")
        index_path = os.path.join(repo_path, "index")

        if not os.path.exists(repo_path):
            raise RuntimeError(
                "Repository not initialized. Run 'delta init' first."
            )

        index = Utils.read_file(index_path)
        index = eval(index) if index else {}

        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"File not found: {file}")

            file_hash = Utils.compute_hash(file)
            index[file] = file_hash
            print(f"Added `{file}` to staging area.")

        Utils.write_file(index_path, str(index))

    @staticmethod
    def status() -> None:
        """
        Prints the contents of the staging area.

        The output is a list of files with their hashes.
        """
        repo_path = ".delta"
        index_path = os.path.join(repo_path, "index")
        index = eval(Utils.read_file(index_path) or "{}")

        print("Staging area:")
        for file, file_hash in index.items():
            print(f"  {file}: {file_hash}")
