# Delta Version Control System

## Introduction
Welcome to **Delta**, a version control system built with Python and inspired by the core functionalities of Git.
Whether managing changes i projects or keeping track ofdevelopment progress, Delta provides a simple and intuitive way to version control your files locally.

Why the name **Delta**? It’s derived from the fourth letter of the Greek alphabet and represents **change** or **difference**—exactly what version control is all about!

While Delta doesn’t have all of Git’s advanced features, it covers core functionalities like initializing repositories, staging files, creating commits, branching and managing commit histories.

### Running `./delta` with No Arguments
When you run `./delta` with no arguments, it will show a list of available commands, along with a brief description of each one. This helps you quickly get familiar with what Delta can do, similar to how Git displays its help when no command is provided.

    $ ./delta

    Delta - A simple version control system

    Available commands:

    init: Initialize a new repository in the current directory.
    add: Add files to the staging area to prepare for commit.
    commit: Commit the staged changes with a message.
    log: Show the commit history of the repository.
    status: Show the current status of the repository (staged/unstaged changes).
    clone: Clone a remote repository into a new directory.
    branch: Create, list, or delete branches.
    checkout: Switch to a different branch.

---

## Features & Usage

### Repository Initialization

- Command: `./delta init`
- Creates a `.delta` directory in the project root, which stores all repository data, including commit history, staged files, and configuration.

When you initialize a repository with `./delta init`, the following directory structure will be created:

```
├── .delta/
│   ├── objects/
│   ├── refs/
│   ├── HEAD
│   └── index
├── .deltaignore
└── <other project files>
```

#### `.delta` Directory Details

-   **`objects/`**: Directory that holds commit objects that store the actual snapshots of the repository at different points in time.
-   **`refs/`**: Directory containing references to branches.
-   **`index`**: File that holds the staged changes (similar to Git's staging area).
-   **`HEAD`**: File that points to the current branch, indicating the state of the repository's working directory.

- `.deltaignore`: File that works similarly to Git's `.gitignore`, by specifying files or directories to exclude from version control by writing patterns in this file. Examples include:

    -   `*.log` – Exclude all `.log` files.
    -   `node_modules/` – Exclude the `node_modules` directory.

### Staging Files

- Command: `./delta add <filename>`
- Adds specified files to the staging area.
- Staged files are recorded in `.delta/index` file.
- To add multile files at once: `./delta add <file1> <file2> <file3>` or `./delta add *.txt`

### Committing Changes

- Command: `./delta commit -m "message"`
- Takes a snapshot of staged files and creates a new commit.
- Stores commit metadata such as hash, parent commit, timestamp, and message.


### Viewing Commit Logs

- Command: `./delta log`
- Displays commit history in reverse chronological order.
- Shows commit hash, timestamp, and message.

### Checking Status

- Command: `./delta status`
- Lists files that are modified, staged, or not tracked compared to the last commit.

### Branch Creation

-   **Command**: `./delta branch <branch_name>`
-   Create new branches to work on features or fixes without affecting the main codebase.
-   Example:
    ```bash
    ./delta branch feature-1
    ```

### Listing Branches

-   **Command**: `./delta branch`
-   Lists all branches in the repository, with an asterisk (*) to indicate the current branch.
-   Example:
    ```bash
    $./delta branch
    *master
    feature-1
    ```

### Switching Branches

-   **Command**: `./delta checkout <branch_name>`
-   Switches to a different branch.
-   Example:
    ```bash
    $./delta checkout feature-1
    $./delta branch
    master
    *feature-1
    ```

### Branch Deletion
-   **Command**: `./delta delete <branch_name>`
-   Deletes a specified branch.
-   Cannot delete the currently active branch.


### Cloning Repositories Locally

- Command: `./delta clone <source_path> <destination_path>`
- Copies the `.delta` directory from one location to another, replicating the repository.

### Ignoring Files

- File: `.deltaignore`
- Users can specify patterns (e.g., `*.log`, `node_modules/`) for files to be excluded from version control.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/lkendi/DeltaVCS.git
   ```

2. Navigate to the project directory
    ```bash
    cd DeltaVCS
    ```
3. Make the `delta` command executable
    ```bash
    chmod +x delta
    ```
4. Now you can use Delta as a command line tool
    ```bash
    ./delta <command>
    ```

## Running Tests

Delta uses Python's built-in `unittest` framework for testing. To run the tests, use the following command:

```bash
PYTHONPATH=src python -m unittest discover tests
```

This command will:

-   Set the `src` directory as the `PYTHONPATH`, so the Python modules in the `src` directory can be imported during tests.
-   Discover and run all tests in the `tests` directory.

Make sure to run this command from the project root directory (where the `src` and `tests` directories are located).

## Comparison with Git

| Feature | Delta | Git |
| --- | --- | --- |
| Repository Init | `delta init` | `git init` |
| Staging Files | `delta add` | `git add` |
| Commit | `delta commit` | `git commit` |
| Log | `delta log` | `git log` |
| Status | `delta status` | `git status` |
| Branching | `delta branch <branch>` | `git branch <branch>`|
| Checkout | `delta checkout <branch>` |  `git checkout <branch>`|
| List Branches | `delta branch` | `git branch` |
| Delete Branch | `delta delete <branch>` | `git branch -d <branch> `|
| Clone | Local only | Remote and local |
| Ignore Files | `.deltaignore` | `.gitignore` |


## Future Enhancements

-   Remote repository support
-   Conflict detection and resolution
