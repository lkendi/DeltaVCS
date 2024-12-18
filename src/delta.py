#!/usr/bin/env python3
"""Delta module - entry point"""
from commit import Commit
from repo import Repository
from branch import Branch
import os
import sys


class Delta:
    """Delta class - parses user commands"""
    def __init__(self) -> None:
        """
        Constructor for the Delta class. Initializes the Delta class by
        setting up a dictionary of commands mapped to their
        corresponding methods.
        """
        self.commands = {
            "init": self.init_repo,
            "add": self.add_files,
            "commit": self.commit_changes,
            "log": self.show_commit_history,
            "status": self.show_status,
            "clone": self.clone_repo,
            "branch": self.handle_branch,
            "checkout": self.handle_checkout,
        }

    def run(self) -> None:
        """
        Parses user commands from command line arguments
        and executes the corresponding function.

        Raises:
            ValueError: If no command is provided or if the command is unknown.
        """
        if len(sys.argv) < 2:
            raise ValueError(
                "No command provided. "
                "Use one of: init, add, commit, log, status, clone."
            )
        command = sys.argv[1]
        if command in self.commands:
            try:
                self.commands[command](*sys.argv[2:])
            except Exception as e:
                print(f"Error: {e}")
        else:
            raise ValueError(f"Unknown command: `{command}`")

    def init_repo(self) -> None:
        """
        Initializes a repository in the current directory.
        """
        try:
            Repository.init()
        except Exception as e:
            print(f"Error: {e}")

    def add_files(self, *files: str) -> None:
        """
        Adds files to the staging area.

        Args:
            *files: A variable number of file paths to add to the staging area.

        Raises:
            ValueError: If no files are provided.
        """
        if not files:
            raise ValueError("No files provided")
        try:
            Repository.add(list(files))
        except Exception as e:
            print(f"Error: {e}")

    def commit_changes(self, *args: str) -> None:
        """
        Commits changes in the staging area.

        Args:
            *args: Command line arguments.
            The first argument must be "-m" and
            the second argument must be the commit message.

        Raises:
            ValueError: If no commit message is provided.
        """
        if len(args) < 2 or args[0] != "-m":
            raise ValueError(
                "Commit message required. Use: delta commit -m 'message'"
            )
        try:
            Commit.create(args[1])
        except Exception as e:
            print(f"Error: {e}")

    def show_commit_history(self) -> None:
        """
        Displays the commit history of the repository.
        """
        try:
            Commit.log()
        except Exception as e:
            print(f"Error: {e}")

    def show_status(self) -> None:
        """
        Checks the status of the repository.
        """
        try:
            Repository.status()
        except Exception as e:
            print(f"Error: {e}")

    def handle_branch(self, *args: str) -> None:
        """
        Handles the branch command.

        Args:
            *args: Command line arguments.
            The first argument specifies the action:
            - "list" for listing branches
            - "delete" to delete a branch
            - Any other argument to create a branch

        Raises:
            ValueError: If no branch name is provided
            or invalid arguments are given.
        """
        if len(args) == 0:
            try:
                Branch.list()
            except Exception as e:
                print(f"Error: {e}")
        elif args[0] == "delete":
            if len(args) < 2:
                raise ValueError(
                    "Branch name required. Use: delta branch delete <name>"
                )
            try:
                Branch.delete(args[1])
            except Exception as e:
                print(f"Error: {e}")
        elif len(args) == 1:
            try:
                Branch.create(args[0])
            except Exception as e:
                print(f"Error: {e}")
        else:
            raise ValueError(
                "Invalid usage. Use 'delta branch', "
                "'delta branch delete <name>', or "
                "'delta branch <name>'"
            )

    def handle_checkout(self, *args: str) -> None:
        """
        Handles the checkout command.

        Args:
            *args: Command line arguments.
            The first argument must be the branch name.

        Raises:
            ValueError: If no branch name is provided.
        """
        if len(args) != 1:
            raise ValueError(
                "Branch name required. Use: delta checkout <name>"
            )
        try:
            Branch.switch(args[0])
        except Exception as e:
            print(f"Error: {e}")

    def clone_repo(self, *args: str) -> None:
        """
        Clones a repository.

        Args:
            *args: Command line arguments.
            The first argument must be the URL of the repository to clone.

        Raises:
            ValueError: If the source path is missing.
        """
        if len(args) < 1:
            raise ValueError(
                "Source path required. Use: delta clone <source> <destination>"
            )
        source_path = args[0]
        if len(args) > 1:
            destination_path = args[1]
        else:
            destination_path = os.path.basename(os.path.abspath(source_path))
        try:
            Repository.clone(source_path, destination_path)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    Delta().run()
