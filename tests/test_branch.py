#!/usr/bin/env python3
"""Branch module - unit tests"""
import unittest
from unittest.mock import patch
import os
from src.branch import Branch


class TestBranch(unittest.TestCase):
    """Branch module unit tests"""

    @patch("os.makedirs")
    @patch("os.path.exists")
    @patch("utils.Utils.is_repo_initialized")
    def test_create_branch_valid(self,
                                 mock_is_repo_initialized,
                                 mock_path_exists,
                                 mock_makedirs):
        mock_is_repo_initialized.return_value = True
        mock_path_exists.side_effect = (
            lambda x: False if x.endswith("new_branch") else True
        )

        with patch("utils.Utils.read_file", return_value="12345"), \
             patch("utils.Utils.write_file") as mock_write_file:

            Branch.create("new_branch")
            mock_makedirs.assert_called_once_with(
                os.path.join(".delta", "refs", "heads"), exist_ok=True
            )
            mock_write_file.assert_called_with(
                os.path.join(".delta", "refs", "heads", "new_branch"), "12345"
            )

    @patch("utils.Utils.is_repo_initialized")
    def test_create_branch_invalid_name(self, mock_is_repo_initialized):
        mock_is_repo_initialized.return_value = True
        with self.assertRaises(ValueError):
            Branch.create("invalid/name")

    @patch("os.makedirs")
    @patch("os.path.exists", side_effect=lambda x: x == os.path.join(
        ".delta", "refs", "heads", "existing_branch"
    ))
    @patch("utils.Utils.is_repo_initialized", return_value=True)
    def test_create_branch_already_exists(self,
                                          mock_is_repo_initialized,
                                          mock_path_exists,
                                          mock_makedirs):
        with patch("builtins.print") as mock_print:
            Branch.create("existing_branch")
            mock_print.assert_called_with(
                "Branch 'existing_branch' already exists."
            )

    @patch("os.path.exists", return_value=False)
    @patch("utils.Utils.is_repo_initialized", return_value=False)
    def test_create_branch_no_repo(self,
                                   mock_is_repo_initialized,
                                   mock_path_exists):
        with self.assertRaises(RuntimeError):
            Branch.create("new_branch")

    @patch("os.path.exists", return_value=True)
    @patch("utils.Utils.read_file", return_value="ref: refs/heads/main")
    def test_current_branch(self,
                            mock_read_file,
                            mock_path_exists):
        current_branch = Branch._current_branch()
        self.assertEqual(current_branch, "main")

    @patch("os.path.exists",
           side_effect=lambda x: x in {".delta/HEAD", ".delta/refs/heads"})
    @patch("utils.Utils.is_repo_initialized", return_value=True)
    @patch("utils.Utils.read_file", return_value="ref: refs/heads/main")
    @patch("os.listdir", return_value=["main", "dev"])
    def test_list_branches(self, mock_listdir,
                           mock_read_file,
                           mock_is_repo_initialized,
                           mock_path_exists):
        with patch("builtins.print") as mock_print:
            Branch.list()
            mock_print.assert_any_call("Branches:")
            mock_print.assert_any_call("* main")
            mock_print.assert_any_call("  dev")

    @patch("os.path.exists",
           side_effect=lambda x: x in (
               ".delta/HEAD",
               ".delta/refs/heads/dev"
           ))
    @patch("utils.Utils.read_file", return_value="ref: refs/heads/main")
    @patch("os.remove")
    def test_delete_branch(self,
                           mock_remove,
                           mock_read_file,
                           mock_path_exists):
        with patch("utils.Utils.is_repo_initialized", return_value=True), \
             patch("branch.Branch._current_branch", return_value="main"):
            Branch.delete("dev")
            mock_remove.assert_called_once_with(
                os.path.join(".delta", "refs", "heads", "dev")
            )


if __name__ == "__main__":
    unittest.main()
