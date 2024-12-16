#!/usr/bin/env python3
"""Reusable functions module"""
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
