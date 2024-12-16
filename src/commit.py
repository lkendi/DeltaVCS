#!/usr/bin/env python3
"""Module that manages commits"""
import hashlib
import time
import os
import json
from utils import Utils


class Commit:
    """Commit class"""
    def __init__(self, message: str, files: dict, parent: str = None) -> None:
        """
        Initializes a new commit instance.

        Args:
            message (str): The commit message.
            parent (str): The hash of the parent commit.
            files (dict): A dictionary of files included in the commit.
        """

        self.message = message
        self.parent = parent
        self.timestamp = time.time()
        self.files = files
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """
        Computes the SHA-1 hash of the commit.

        The hash is computed from the commit message, parent hash,
        timestamp, and a JSON representation of the files included
        in the commit.

        Returns:
            str: The SHA-1 hash of the commit.
        """
        content = (
            f"{self.message}"
            f"{self.parent}"
            f"{self.timestamp}"
            f"{json.dumps(self.files, sort_keys=True)}"
        )
        return hashlib.sha1(content.encode()).hexdigest()

    @staticmethod
    def create(message: str) -> None:
        """
        Creates a new commit.

        Args:
            message (str): The commit message.

        Raises:
            RuntimeError: If the repository is not initialized
            or staging area is empty.
        """
        repo_path = ".delta"
        objects_path = os.path.join(repo_path, "objects")
        index_path = os.path.join(repo_path, "index")
        head_path = os.path.join(repo_path, "HEAD")

        if not os.path.exists(repo_path):
            raise RuntimeError(
                "Repository not initialized. Run 'delta init' first."
            )

        index = eval(Utils.read_file(index_path) or "{}")
        if not index:
            raise RuntimeError("No changes staged for commit.")

        parent = Utils.read_file(head_path)

        commit = Commit(message=message, parent=parent, files=index)
        obj_path = os.path.join(objects_path, commit.hash)
        Utils.write_file(obj_path, json.dumps(commit.__dict__))
        Utils.write_file(head_path, commit.hash)

        index_keys = list(index.keys())
        for file in index_keys:
            del index[file]

        Utils.write_file(index_path, str(index))
        print(f"Commit created: {commit.hash}")

    @staticmethod
    def log() -> None:
        """
        Displays the commit logs in reverse chronological order.

        Raises:
            RuntimeError: If the repository is not initialized
            or no commits exist.
        """
        repo_path = ".delta"
        objects_path = os.path.join(repo_path, "objects")
        head_path = os.path.join(repo_path, "HEAD")

        if not os.path.exists(repo_path):
            raise RuntimeError(
                "Repository not initialized. Run 'delta init' first."
            )

        head = Utils.read_file(head_path)
        if not head:
            raise RuntimeError("No commits found in the repository.")

        print("\033[1mCommit log:\033[0m\n")

        while head:
            if head.startswith("ref: "):
                ref_path = os.path.join(repo_path, head[5:])
                head = Utils.read_file(ref_path)

            commit_file_path = os.path.join(objects_path, head)
            commit_data = Utils.read_file(commit_file_path)
            if not commit_data:
                break

            commit = json.loads(commit_data)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S',
                                      time.localtime(commit["timestamp"]))

            print(f"\033[32mCommit:{head}")
            print(f"\033[33mDate:{timestamp}")
            print(f"\033[34mMessage:\033[0m {commit['message']}")
            print(f"\033[35mParent:\033[0m {commit['parent']}\n")

            head = commit["parent"]
