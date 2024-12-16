# Delta: A Distributed Version Control System

## Introduction
Welcome to **Delta**, a distributed version control system built with Python and inspired by the core functionalities of Git. 
Whether managing changes i projects or keeping track ofdevelopment progress, Delta provides a simple and intuitive way to version control your files locally.

Why the name **Delta**? It’s derived from the fourth letter of the Greek alphabet and represents **change** or **difference**—exactly what version control is all about!

While Delta doesn’t have all of Git’s advanced features, it covers core functionalities like initializing repositories, staging files, creating commits, branching and managing commit histories.


---

## Features

### Repository Initialization

- Command: `delta init`
- Creates a `.delta` directory in the project root, which stores all repository data, including commit history, staged files, and configuration.

### Staging Files

- Command: `delta add <file>`
- Adds specified files to the staging area.
- Staged files are recorded in `.delta/index` file.

### Committing Changes

- Command: `delta commit -m "message"`
- Takes a snapshot of staged files and creates a new commit.
- Stores commit metadata such as hash, parent commit, timestamp, and message.


### Viewing Commit Logs

- Command: `delta log`
- Displays commit history in reverse chronological order.
- Shows commit hash, timestamp, and message.

### Checking Status

- Command: `delta status`
- Lists files that are modified, staged, or not tracked compared to the last commit.

### Branching

-   **Command**: `delta branch <branch_name>`
-   Create new branches to work on features or fixes without affecting the main codebase.
-   Switch between branches seamlessly.

### Cloning Repositories Locally

- Command: `delta clone <source_path> <destination_path>`
- Copies the `.delta` directory from one location to another, replicating the repository.

### Ignoring Files

- File: `.deltaignore`
- Users can specify patterns (e.g., `*.log`, `node_modules/`) for files to be excluded from version control.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/username/DeltaVCS.git
   ```

2. Navigate to the project directory
    ```bash
    cd DeltaVCS
    ```
3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Comparison with Git

| Feature | Delta | Git |
| --- | --- | --- |
| Repository Init | `delta init` | `git init` |
| Staging Files | `delta add` | `git add` |
| Commit | `delta commit` | `git commit` |
| Log | `delta log` | `git log` |
| Status | `delta status` | `git status` |
| Branching | `delta branch <branch>` | `git branch <branch>`
| Clone | Local only | Remote and local |
| Ignore Files | `.deltaignore` | `.gitignore` |


## Future Enhancements

-   Remote repository support
-   Conflict resolution
