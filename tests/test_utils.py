#!/usr/bin/env python3
"""Utils module - unit tests"""
import hashlib
import os
import unittest
from unittest.mock import patch
from src.utils import Utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = "test_dir"
        self.test_file = "test_file.txt"
        self.test_content = "Hello, World!"
        self.test_hash = hashlib.sha1(self.test_content.encode()).hexdigest()

        if not os.path.exists(self.test_dir):
            os.mkdir(self.test_dir)

        with open(self.test_file, "w") as f:
            f.write(self.test_content)

    def tearDown(self):
        """Clean up test files and directories."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_compute_hash(self):
        """Test the compute_hash method."""
        self.assertEqual(Utils.compute_hash(self.test_file), self.test_hash)

    def test_compute_hash_file_not_found(self):
        """Test compute_hash raises FileNotFoundError for missing file."""
        with self.assertRaises(FileNotFoundError):
            Utils.compute_hash("non_existent_file.txt")

    @patch("os.path.exists", return_value=True)
    def test_is_repo_initialized_true(self, mock_exists):
        """Test is_repo_initialized when repo is initialized."""
        self.assertTrue(Utils.is_repo_initialized())

    @patch("os.path.exists", return_value=False)
    def test_is_repo_initialized_false(self, mock_exists):
        """Test is_repo_initialized when repo is not initialized."""
        self.assertFalse(Utils.is_repo_initialized())

    def test_create_directory(self):
        """Test create_directory method."""
        path = os.path.join(self.test_dir, "new_dir")
        Utils.create_directory(path)
        self.assertTrue(os.path.exists(path))
        os.rmdir(path)

    def test_read_file(self):
        """Test read_file method."""
        content = Utils.read_file(self.test_file)
        self.assertEqual(content, self.test_content)

    def test_read_file_not_found(self):
        """Test read_file raises FileNotFoundError for missing file."""
        with self.assertRaises(FileNotFoundError):
            Utils.read_file("non_existent_file.txt")

    def test_write_file(self):
        """Test write_file method."""
        new_file = "new_file.txt"
        Utils.write_file(new_file, self.test_content)
        with open(new_file, "r") as f:
            content = f.read()
        self.assertEqual(content, self.test_content)
        os.remove(new_file)

    def test_matches_pattern_true(self):
        """Test matches_pattern returns True for matching patterns."""
        self.assertTrue(Utils.matches_pattern("dir/file.txt", "dir/*.txt"))

    def test_matches_pattern_false(self):
        """Test matches_pattern returns False for non-matching patterns."""
        self.assertFalse(Utils.matches_pattern("dir/file.txt", "dir/*.jpg"))


if __name__ == "__main__":
    unittest.main()
