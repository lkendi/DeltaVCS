#!/usr/bin/env python3
"""Reusable functions module"""
from config import DELTA_DIR
import fnmatch
import hashlib
import os


class Utils:
    @staticmethod
    def compute_hash(file_path: str) -> str:
        """
        Computes the SHA-1 hash of a file.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The SHA-1 hash of the file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()

    @staticmethod
    def is_repo_initialized() -> bool:
        """
        Checks if the repository is initialized.

        Returns:
            bool: True if the repository is initialized, False otherwise.
        """
        return os.path.exists(DELTA_DIR)

    @staticmethod
    def create_directory(path: str) -> None:
        """
        Creates a directory if it does not exist.

        Args:
            path (str): The path of the directory to create.
        """
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Reads the content of a file as a string.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The content of the file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r") as f:
            return f.read()

    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """
        Writes a string to a file.

        Args:
            file_path (str): The path to the file.
            content (str): The content to write to the file.
        """
        with open(file_path, "w") as f:
            f.write(content)

    @staticmethod
    def matches_pattern(file_path: str, pattern: str) -> bool:
        """
        Checks if a file path matches a pattern.

        Args:
            file_path (str): The file path to check.
            pattern (str): The pattern to match.

        Returns:
            bool: True if the file path matches the pattern, False otherwise.
        """
        file_path = os.path.normpath(file_path)
        pattern = os.path.normpath(pattern)

        return fnmatch.fnmatch(file_path, pattern)
