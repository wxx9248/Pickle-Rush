# Development Environment

## Python version

Please use Python 3.10 for consistent and complete support.
Older or newer versions may bring problems.

Note: the last label for the version number (PATCH) is not important.
One can use the latest version of Python 3.10, which is so far 3.10.9.
Please refer to https://semver.org/ for details for semantic versioning.

## About virtual environment

The project uses Python virtual environment to maintain environment consistency.
Please refer to https://docs.python.org/3.10/library/venv.html for documentation.

### Initializing virtual environment

* Open a terminal inside the project root
    * Install `virtualenv` module if you haven't:
      ```bash
      pip3 install virtualenv
      ```
    * Initialize a virtual environment for the project:
      ```bash
      python3 -m virtualenv venv
      ```
    * Enable the virtual environment for this terminal session:
        * For command line shells, a developer should initialize the environment by sourcing
          corresponding `activate` script residing in `venv/bin`. Typically:
            * For Windows, execute `.\venv\bin\activate.ps1` in a Windows Powershell terminal;
            * For Linux/macOS, execute `source venv/bin/activate` in a bash/zsh terminal.
    * Install dependencies
      ```bash
      pip3 install -r requirements.txt
      ```
    * Open the project in your IDE. Your IDE should recognize the virtual environment and
      use it upon opening the project.

# General Workflow

1. Pull master branch before doing anything: `git pull`
2. Checkout a new branch: `git checkout -b your-branch-name`
3. Make changes
4. Add and commit changes: `git add . && git commit`
5. Push changes to the remote branch: `git push`
6. Open a pull request
7. Request for peer review
8. Merge in to master branch

# Coding Standards

1. Format your code before committing changes.
2. Annotate type of every variable if possible.
3. No deep nesting in the code.
   If you find your code uses more than 4 indentations, you need to cut it down possibly by:
    * Converting `if-else` statements to `if` guards;
    * Refactoring the logic into smaller functions;
    * Use [`itertools`](https://docs.python.org/3/library/itertools.html) to flatten loops;
4. Write good comments when code cannot document itself.
5. Use private fields and property decorator for class attributes
