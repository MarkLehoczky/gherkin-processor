<div align="center">

# GHERKIN PROCESSOR

**Gherkin Processor** is a *Python* package that processes *Gherkin* files into *Python* dataclasses. It provides utilities for validating, processing, and saving *Gherkin* in both text and *Json* formats.

---

[![License][license-badge]][license-link]
[![Release][release-badge]][release-link]

[![Build][build-badge]][build-link]
[![Issue][issue-badge]][issue-link]

[![Python Versions][python-badge]](#)
[![OS Versions][os-badge]](#)

---

</div>

## Features

- Gherkin content processing into modular Python dataclasses
- Gherkin syntax validation
- I/O operations for loading Gherkin files and saving Gherkin content either with Gherkin syntax or with Json syntax
- Command line execution for Gherkin file processing, validation and I/O operations

## Installation

You can install the **Gherkin Processor** package by cloning the repository or downloading from the releases.

### Clone the Repository

> Requirements:
> - [git](https://git-scm.com/downloads) is installed and added to PATH
> - [Python 3.10+](https://www.python.org/downloads/) version is installed and added to PATH
> - [pip](https://pypi.org/project/pip/) is installed and added to PATH (often already installed with Python)

```sh
# 1. Clone the repository
git clone https://github.com/MarkLehoczky/gherkin-processor.git

# 2. Navigate to the cloned directory
cd gherkin-processor

# 3. Install the package
python -m pip install .

# (Optional) 4. Install the necessary python packages for pre-commit hook
python -m pip install -r requirements.txt

# (Optional) 5. Change the git pre-commit hook to the custom pre-commit configuration
pre-commit install
```

### Download from Releases

> Requirements:
> - [Python 3.10+](https://www.python.org/downloads/) version is installed and added to PATH
> - [pip](https://pypi.org/project/pip/) is installed and added to PATH (often already installed with Python)

1. Go to the [Releases](https://github.com/MarkLehoczky/gherkin-processor/releases) page.
2. Download the latest release.
3. Extract the downloaded file.
4. Navigate to the extracted directory.
5. Install the package by clicking on the install file
    - *Windows file*: "Windows_installer"
    - *Linux file*: "Linux_installer"
    - *MacOS file*: **Not available**, can be created by compiling the [install_package.py](./install_package.py) script

## Usage

> [!WARNING]  
> The examples are not implemented yet. The links will navigate to a 404 error page.

### Command Line Interface

The **Gherkin Processor** can be used via the command line interface (CLI).

```sh
gherkin-processor [-h] -i INPUT [-o OUTPUT] [-p] [-s] [-j] [-y] [-v]
```

#### Options

```text
-h, --help                  show this help message and exit
-i, --input INPUT           input file path
-o, --output OUTPUT         output file of the savings
-p, --print                 write the input file Gherkin syntax to standard output
-s, --save, --save-gherkin  save file as Gherkin
-j, --json, --save-json     save file as JSON
-y, --yes, --force-yes      automatically press 'y' for every user input request
-v, --validate              validate the input file syntax
```

See the [CLI examples](examples/command_line_interface.ipynb) for details.

### Python Module

The **Gherkin Processor** can also be used programmatically in a Python code.

```python
from gherkin_processor.util import process, save, validate

# Example Gherkin text
gherkin_text = """
Feature: User login
  Scenario: Successful login
    Given the user navigates to the login page
    When the user enters valid credentials
    Then the user should be redirected to the dashboard"""

# Process the Gherkin text
gherkin = process(gherkin_text)

# Validate the Gherkin text (with an exception raised if invalid)
try:
    validate(gherkin_text)
    print("Gherkin text is valid.")
except Exception as e:
    print(f"Gherkin text validation failed: {e}")

# Save the processed Gherkin object to a file with Gherkin syntax
save(gherkin, "user_login.feature", "GHERKIN")
# Save the processed Gherkin object to a file with Json syntax
save(gherkin, "user_login.json", "JSON")
```

See the [Module examples](examples/modules.ipynb) and [Data class structure](examples/classes.ipynb) for details.

## License

This project is licensed under [MIT License](LICENSE).

[license-link]:  https://github.com/MarkLehoczky/gherkin-processor/blob/main/LICENSE
[release-link]:  https://github.com/MarkLehoczky/gherkin-processor/releases
[build-link]:https://github.com/MarkLehoczky/gherkin-processor/actions
[issue-link]:   https://github.com/MarkLehoczky/gherkin-processor/issues

[license-badge]: https://img.shields.io/github/license/marklehoczky/gherkin-processor?style=for-the-badge&color=success
[release-badge]: https://img.shields.io/github/v/release/marklehoczky/gherkin-processor?include_prereleases&sort=date&display_name=tag&style=for-the-badge&color=success
[build-badge]:   https://img.shields.io/github/actions/workflow/status/marklehoczky/gherkin-processor/ci_main.yml?style=for-the-badge
[issue-badge]:  https://img.shields.io/github/issues/marklehoczky/gherkin-processor?style=for-the-badge
[python-badge]:  https://img.shields.io/badge/Python-3.10_%7C_latest-blue?style=for-the-badge
[os-badge]:  https://img.shields.io/badge/OS-Windows_%7C_Linux_%7C_MacOS-blue?style=for-the-badge
