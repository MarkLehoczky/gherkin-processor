<div align="center">

# GHERKIN PROCESSOR

**Gherkin Processor** is a Python package that processes Gherkin files into Python *dataclasses*. It provides utilities for validating, processing, and saving Gherkin scenarios in both text and JSON formats.

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

- Gherkin scenario validation
- Gherkin scenario syntax issue description
- Gherkin scenario content processing into Python dataclass
- Save processed scenarios in text or JSON format
- Directly load scenarios from file paths

## Installation

You can install the **Gherkin Processor** package by cloning the repository or downloading from the releases.

> Requirements:
> - Python 3.10+ version with pip installed

### Clone the Repository

```sh
# 1. Clone the repository
git clone https://github.com/MarkLehoczky/gherkin-processor.git

# 2. Navigate to the cloned directory
cd gherkin-processor

# 3. Install the package via 'pip'
pip install .

# (Optional) 4. Set up pre-commit git hook
cp hooks/pre-commit .git/hooks/pre-commit
```

### Download from Releases

1. Go to the [Releases](https://github.com/MarkLehoczky/gherkin-processor/releases) page.
2. Download the latest release.
3. Extract the downloaded file.
4. Navigate to the extracted directory.
5. Install the package by clicking on the "[Install.bat](./Install.bat)" file

## Usage

### Command Line Interface

The **Gherkin Processor** can be used via the command line interface (CLI).

```sh
gherkin-processor [-h] -i INPUT [-p] [-s] [--save-as-json] [--validate]
```

#### Options

```text
-h, --help                 show this help message and exit
-i INPUT, --input INPUT    specify the input Gherkin file location to process
-p, --print                print the processed Gherkin scenario to the standard output
-s, --save                 save the processed Gherkin scenario to a file
--save-as-json             save the processed Gherkin scenario to a file in JSON format
--validate                 validate the input Gherkin file syntax
```

See the [CLI examples](examples/cli.ipynb) for details.

### Python API

The **Gherkin Processor** can also be used programmatically in a Python code.

```python
from gherkin_processor.utils import scenario    # file
from gherkin_processor.scenario import Scenario # class

# Load and process the scenario from a file
processed_scenario: Scenario = scenario.load("path/to/scenario.feature")

# Save the processed scenario to a file
scenario.save(processed_scenario, "path/to/saved_scenario.feature")
```

See the [API examples](examples/api.ipynb) and [Data class structure](examples/data.ipynb) for details.

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
