#!/usr/bin/env python3
"""Delta module - parses user commands"""
from commit import Commit
from repo import Repository
import sys


class Delta:
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
        Repository.init()

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
        Repository.add(list(files))

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
        Commit.create(args[1])

    def show_commit_history(self) -> None:
        """
        Displays the commit history of the repository.
        """
        Commit.log()

    def show_status(self) -> None:
        """
        Checks the status of the repository.
        """
        Repository.status()

    def clone_repo(self, *args: str) -> None:
        """
        Clones a repository.

        Args:
            *args: Command line arguments.
            The first argument must be the URL of the repository to clone.

        Raises:
            ValueError: If no URL is provided.
        """
        if len(args) < 1:
            raise ValueError("URL required. Use: delta clone <url>")
        Repository.clone(args[0])


if __name__ == "__main__":
    Delta().run()
