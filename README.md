<div align="center">

# GHERKIN PROCESSOR

**Gherkin Processor** is a *Python* package that processes *Gherkin* files into *Python* dataclasses. It provides utilities for validating, processing, and saving *Gherkin* in both text and *JSON* formats.

---

[![License][license-badge]][license-link]
[![Release][release-badge]][release-link]

[![Build][build-badge]][build-link]
[![Issue][issue-badge]][issue-link]

[![Python Versions][python-badge]](#)
[![OS Versions][os-badge]](#)

---

</div>

## Implemented & Planned Features

**Gherkin Content**

- [x] Convert Gherkin content into Python classes
- [x] Validate Gherkin syntax
- [x] Convert processed Gherkin content back into Gherkin syntax
- [x] Convert processed Gherkin content into JSON format
- [ ] Support optional alternative keywords for repeated steps when converting to Gherkin syntax
- [ ] Support optional indentation when converting to Gherkin syntax
- [ ] Optionally exclude `None` values when converting to JSON

**Input & Output (I/O) Operations**

- [x] Load and process Gherkin files
- [x] Save Gherkin content in Gherkin syntax
- [x] Save Gherkin content in JSON format
- [ ] Load and process Gherkin content from JSON files

**Command-Line Interface (CLI)**

- [x] Process Gherkin files
- [x] Validate Gherkin files
- [x] Print Gherkin content
- [x] Save Gherkin content in Gherkin syntax
- [x] Save Gherkin content in JSON format
- [ ] Support batch processing for all files in a directory
- [ ] Support recursive batch processing for directories and subdirectories

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

# 3. Install the package (with editable install)
pip install -e .

# (Optional) 4. Install the necessary python packages for pre-commit hook
pip install -r requirements.txt

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
5. Run the installer based on the operating system
    - **Windows**: Run `Windows_installer.exe`
    - **Linux**: Run `./Linux_installer`
    - **MacOS**: ***Not available***
    - *Alternative solutions:*
        - Run the Python installation script:
          ```sh
          python ./install_package.py
          ```
        - Compile the script into an executable:
          ```sh
          pip install pyinstaller
          pyinstaller --onefile ./install_package.py
          ./dist/install_package
          ```

## Usage

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

See the CLI [documentation](docs/cli.md) and [examples](examples/cli.ipynb) for details.

### Python Module

The **Gherkin Processor** can also be used programmatically in a Python code.

```python
from gherkin_processor.util import process, save, validate

# Example Gherkin text
gherkin_text = """Feature: User login

  Scenario: Login attempt with valid credentials
    Given I navigate to the login page
    When I enter the username "user@example.com"
    And I enter the password "password123"
    Then I am navigated to the homepage"""

# Validate the Gherkin text (with an exception raised if invalid)
try:
    validate(gherkin_text)
    print("Gherkin text is valid.")
except ValueError as e:
    print(f"Gherkin text validation failed: {e}")

# Process the Gherkin text
gherkin = process(gherkin_text, validate=False)

# Save the processed Gherkin object to a file with Gherkin syntax
save(gherkin, "user_login.feature", "GHERKIN")
# Save the processed Gherkin object to a file with JSON syntax
save(gherkin, "user_login.json", "JSON")
```

See the Module [documentation](docs/modules.md) and [examples](examples/modules.ipynb) and the Data class structure [documentation](docs/classes.md) and [examples](examples/classes.ipynb) for details.

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
