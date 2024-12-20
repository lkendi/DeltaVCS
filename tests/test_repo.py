#!/usr/bin/env python3
"""Repo module - unit tests"""
import unittest
import os
import json
from unittest.mock import patch, mock_open, MagicMock
from src.repo import Repository
from src.config import DELTA_DIR, OBJECTS_DIR, REFS_DIR, HEAD_FILE, INDEX_FILE
import shutil


class TestRepository(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.repo_path = "."
        self.files_to_add = ["file1.txt", "file2.txt"]
        self.test_content = "Test file content"

        for file in self.files_to_add:
            with open(file, "w") as f:
                f.write(self.test_content)

    def tearDown(self):
        """Clean up test files and directories."""
        for file in self.files_to_add:
            if os.path.exists(file):
                os.remove(file)

        if os.path.exists(DELTA_DIR):
            shutil.rmtree(DELTA_DIR)

    @patch("os.path.exists", return_value=False)
    @patch("utils.Utils.create_directory")
    @patch("utils.Utils.write_file")
    def test_init_success(self, mock_write, mock_create_dir, mock_exists):
        """Test repository initialization."""
        self.assertTrue(Repository.init(self.repo_path))
        mock_create_dir.assert_any_call(OBJECTS_DIR)
        mock_create_dir.assert_any_call(REFS_DIR)
        mock_write.assert_any_call(HEAD_FILE, "ref: refs/heads/master\n")
        mock_write.assert_any_call(INDEX_FILE, "{}")

    @patch("os.path.exists", return_value=True)
    def test_init_already_initialized(self, mock_exists):
        """Test repository initialization when already initialized."""
        self.assertFalse(Repository.init(self.repo_path))

    @patch("utils.Utils.is_repo_initialized", return_value=True)
    @patch("utils.Utils.read_file", return_value="{}")
    @patch("utils.Utils.write_file")
    @patch(
        "utils.Utils.compute_hash",
        return_value="dummyhash"
    )
    def test_add_files(self,
                       mock_hash,
                       mock_write,
                       mock_read,
                       mock_initialized):
        """Test adding files to the staging area."""
        Repository.add(self.files_to_add)
        expected_index = {file: "dummyhash" for file in self.files_to_add}
        mock_write.assert_called_with(INDEX_FILE, json.dumps(expected_index))

    @patch("utils.Utils.is_repo_initialized", return_value=False)
    def test_add_files_repo_not_initialized(self, mock_initialized):
        """Test adding files when the repository is not initialized."""
        with self.assertRaises(RuntimeError):
            Repository.add(self.files_to_add)

    @patch("utils.Utils.is_repo_initialized", return_value=True)
    @patch("utils.Utils.read_file", return_value="{}")
    @patch("utils.Utils.write_file")
    @patch("utils.Utils.compute_hash", return_value="dummyhash")
    def test_add_single_file(self,
                             mock_hash,
                             mock_write,
                             mock_read,
                             mock_initialized):
        """Test adding a single file to the staging area."""
        Repository.add([self.files_to_add[0]])
        expected_index = {self.files_to_add[0]: "dummyhash"}
        mock_write.assert_called_with(INDEX_FILE, json.dumps(expected_index))

    @patch("utils.Utils.is_repo_initialized", return_value=True)
    @patch("utils.Utils.read_file", return_value="{}")
    @patch("utils.Utils.write_file")
    @patch("utils.Utils.compute_hash", return_value="dummyhash")
    def test_add_multiple_files(self,
                                mock_hash,
                                mock_write,
                                mock_read,
                                mock_initialized):
        """Test adding multiple files to the staging area."""
        Repository.add(self.files_to_add)
        expected_index = {file: "dummyhash" for file in self.files_to_add}
        mock_write.assert_called_with(INDEX_FILE, json.dumps(expected_index))

    @patch("utils.Utils.is_repo_initialized", return_value=True)
    def test_add_file_not_found(self, mock_initialized):
        """Test adding a non-existent file to the staging area."""
        non_existent_file = "nonexistent.txt"
        with self.assertRaises(FileNotFoundError):
            Repository.add([non_existent_file])

    @patch("utils.Utils.is_repo_initialized", return_value=True)
    @patch(
        "utils.Utils.read_file",
        return_value=json.dumps({"file1.txt": "hash1"})
    )
    def test_status(self, mock_read, mock_initialized):
        """Test printing the status of the staging area."""
        with patch("builtins.print") as mock_print:
            Repository.status()
            mock_print.assert_any_call("Staging area:")
            mock_print.assert_any_call("  file1.txt: hash1")

    @patch("os.path.exists")
    @patch("os.path.isdir")
    @patch("shutil.copytree")
    @patch("src.repo.Repository._load_ignore_patterns",
           return_value=["*.ignore"])
    @patch("src.repo.Repository._is_ignored", return_value=False)
    def test_clone_success(self,
                           mock_is_ignored,
                           mock_load_ignore_patterns,
                           mock_copytree, mock_isdir,
                           mock_path_exists):
        source_path = "source"
        destination_path = "destination"

        def mock_exists_side_effect(path):
            if path == source_path:
                return True
            if path == os.path.join(source_path, ".delta"):
                return True
            return False

        mock_path_exists.side_effect = mock_exists_side_effect
        mock_isdir.side_effect = lambda path: path == source_path

        Repository.clone(source_path, destination_path)

        mock_copytree.assert_called_once_with(
            source_path,
            destination_path,
            ignore=unittest.mock.ANY
        )
        mock_load_ignore_patterns.assert_called_once_with(source_path)

    @patch("os.path.exists", return_value=False)
    def test_clone_source_invalid(self, mock_exists):
        """Test cloning from an invalid source repository."""
        with self.assertRaises(ValueError):
            Repository.clone("invalid_source", "destination")

    @patch("os.path.exists", side_effect=lambda path: path == "source/.delta")
    def test_clone_destination_exists(self, mock_exists):
        """Test cloning to an already existing destination."""
        with self.assertRaises(ValueError):
            Repository.clone("source", "source")

    def test_load_ignore_patterns_no_file(self):
        """Test loading ignore patterns when .deltaignore is missing."""
        patterns = Repository._load_ignore_patterns(self.repo_path)
        self.assertEqual(patterns, [])

    def test_load_ignore_patterns_with_file(self):
        """Test loading ignore patterns from .deltaignore."""
        with open(".deltaignore", "w") as f:
            f.write("*.pyc\n__pycache__/\n")
        patterns = Repository._load_ignore_patterns(self.repo_path)
        os.remove(".deltaignore")
        self.assertEqual(patterns, ["*.pyc", "__pycache__/"])

    @patch(
        "src.utils.Utils.matches_pattern",
        side_effect=lambda file, pattern: pattern in file
    )
    def test_is_ignored(self, mock_matches):
        """Test checking if a file is ignored."""
        patterns = ["*.pyc", "__pycache__/"]
        self.assertTrue(Repository._is_ignored("test.pyc", patterns))
        self.assertFalse(Repository._is_ignored("test.py", patterns))


if __name__ == "__main__":
    unittest.main()
