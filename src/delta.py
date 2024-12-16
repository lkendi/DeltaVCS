#!/usr/bin/env python3
"""Delta module - parses user commands"""
from commit import Commit
from repo import Repository
from staging_area import StagingArea
import sys


class Delta:
    def __init__(self):
        """
        Constructor for the Delta class. Initializes the Delta class by
        setting up a dictionary of commands mapped to their
        corresponding methods. These commands include:
        - "init" for initializing a repository,
        - "add" for adding files to the staging area,
        - "commit" for committing changes,
        - "log" for viewing commit history,
        - "status" for checking the status of the repository,
        - "clone" for cloning an existing repository.
        """

        self.commands = {
            "init": self.init_repo,
            "add": self.add_files,
            "commit": self.commit_changes,
            "log": self.show_commit_history,
            "status": self.show_status,
            "clone": self.clone_repo
        }

    def run(self):
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
            self.commands[command](*sys.argv[2:])
        else:
            raise ValueError(f"Unknown command: {command}")

    def init_repo(self):
        """
        Initializes a repository in the current directory. Called
        when the user runs the "init" command in the command line.
        """
        Repository.init()

    def add_files(self, *files):
        """
        Adds files to the staging area.
        Called when the user runs the "add" command.

        Args:
            *files: A variable number of file paths to add to the staging area.

        Raises:
            ValueError: If no files are provided.
        """
        if not files:
            raise ValueError("No files provided")
        StagingArea.add_files(files)

    def commit_changes(self, *args):
        """
        Commits changes in the staging area.
        Called when the user runs the "commit" command.

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

    def show_commit_history(self):
        """
        Displays the commit history of the repository.
        Called when the user runs the "log" command.
        """
        Commit.log()

    def show_status(self):
        """
        Checks the status of the repository.
        Called when the user runs the "status" command.
        """
        Repository.status()

    def clone_repo(self, *args):
        """
        Clones a repository.
        Called when the user runs the "clone" command.

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
