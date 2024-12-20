#!/usr/bin/env python3
"""Module that manages commits"""
from config import DELTA_DIR, OBJECTS_DIR, INDEX_FILE, HEAD_FILE, BRANCH_DIR
import hashlib
import json
import os
import time
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
        if not Utils.is_repo_initialized():
            raise RuntimeError(
                "Repository not initialized. Run 'delta init' first."
            )

        index = json.loads(Utils.read_file(INDEX_FILE) or "{}")
        if not index:
            raise RuntimeError("No changes staged for commit.")

        head_ref = Utils.read_file(HEAD_FILE).strip()
        if not head_ref:
            head_ref = "ref: refs/heads/master"
            Utils.write_file(HEAD_FILE, head_ref)

        if head_ref.startswith("ref: refs/heads/"):
            branch_name = head_ref[len("ref: refs/heads/"):].strip()
            branch_ref_path = os.path.join(BRANCH_DIR, branch_name)
            parent = (
                Utils.read_file(branch_ref_path).strip()
                if os.path.exists(branch_ref_path)
                else None
            )
        else:
            parent = head_ref

        commit = Commit(message=message, parent=parent, files=index)
        obj_path = os.path.join(OBJECTS_DIR, commit.hash)
        Utils.write_file(obj_path, json.dumps(commit.__dict__))

        if head_ref.startswith("ref: refs/heads/"):
            os.makedirs(BRANCH_DIR, exist_ok=True)
            branch_ref_path = os.path.join(BRANCH_DIR, branch_name)
            Utils.write_file(branch_ref_path, commit.hash)

        index.clear()
        Utils.write_file(INDEX_FILE, json.dumps(index))
        print(f"Commit created: {commit.hash}")

    @staticmethod
    def log() -> None:
        """
        Displays the commit logs in reverse chronological order.

        Raises:
            RuntimeError: If the repository is not initialized
            or no commits exist.
        """
        if not Utils.is_repo_initialized():
            raise RuntimeError(
                "Repository not initialized. Run 'delta init' first."
            )

        head = Utils.read_file(HEAD_FILE).strip()
        if not head:
            raise RuntimeError("No commits found in the repository.")

        print("\033[1mCommit log:\033[0m\n")

        while head:
            if head.startswith("ref: "):
                ref_path = os.path.join(DELTA_DIR, head[5:].strip())
                if not os.path.exists(ref_path):
                    print(f"Branch reference file not found: {ref_path}")
                    break
                head = Utils.read_file(ref_path).strip()

            commit_file_path = os.path.join(OBJECTS_DIR, head)
            commit_data = Utils.read_file(commit_file_path)
            if not commit_data:
                break

            commit = json.loads(commit_data)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S',
                                      time.localtime(commit["timestamp"]))

            print(f"\033[32mCommit: {head}")
            print(f"\033[33mDate: {timestamp}")
            print(f"\033[34mMessage:\033[0m {commit['message']}")
            print(f"\033[35mParent:\033[0m {commit['parent']}\n")

            head = commit["parent"]
