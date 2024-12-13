<div align="center">

# GHERKIN PROCESSOR

A Python package that converts Gherkin scenarios into Python dataclass objects. It offers flexible conversion with strict or relaxed validation of the Gherkin syntax.

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

- Converts Gherkin scenarios into Python `dataclasses` for easy manipulation and analysis.
- Supports strict format validation, ensuring the Gherkin scenarios follow the correct syntax.
- Allows conversion of scenarios even with minor syntax errors, making it more robust.
- Built-in flexibility for customization and extension.

## Installation

```shell
# 1. Clone the Github repository
git clone https://github.com/MarkLehoczky/gherkin-processor.git

# 2. Install package with pip
pip install gherkin-processor
```

## Usage

### Script

```python
from dataclasses import asdict
from json import dumps

from gherkin_processor.utils import scenario
from gherkin_processor.scenario import Scenario

# Loads a Gherkin scenario from a file and processes it into a python data class.
with open("scenario.txt", "r", encoding="utf-8") as scenario_text_file:
    scenario_text: str = scenario_text_file.read()
    scenario_instance: Scenario = scenario.process(scenario_text)

    # Prints some of the scenario components to the standard output.
    print(", ".join(scenario_instance.tags))
    print(scenario_instance.name)

    # Converts the scenario into dictionary format, then saves it as a json.
    with open("scenario.json", "w") as scenario_json_file:
        scenario_json: dict = asdict(scenario_instance)
        scenario_json_file.write(dumps(scenario_json, indent=4))
```

## Dataclass Structure

The resulting Python dataclass structure represents the Gherkin scenario hierarchy. Here's an example of what the structure looks like:

```python
@dataclass
class Scenario:
    tags: List[str]
    name: str
    steps: List[Dict[str, Dict[str, List[str]] | str]]
    template_table: Optional[Dict[str, List[str]]]
```

*Depending whether a step is followed by docstring or table, the `steps` variable's structure may change.*

## Prerequisites

### Mandatory

- Python 3.10 or newer version

### Advised

#### VSCode extensions

The following extensions are listed in the `.vscode/extensions.json` file.

- [autoDocstring - Python Docstring Generator](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
- [autoflake](https://marketplace.visualstudio.com/items?itemName=mikoz.autoflake-extension)
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Mypy Type Checker](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
- [Python Docstring Highlighter](https://marketplace.visualstudio.com/items?itemName=rodolphebarbanneau.python-docstring-highlighter)
- [Python Test Explorer for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=littlefoxteam.vscode-python-test-adapter)
- [Python Type Hint](https://marketplace.visualstudio.com/items?itemName=njqdev.vscode-python-typehint)

#### Python packages

The following packages are listed in the `requirements.txt` file.
To install them simply use the following command:

```shell
pip install -r requirements.txt
```

- pylint
- mypy
- pyflakes
- radon
- black
- pycodestyle
- pydocstyle
- bandit
- pytest
- pytest-cov

## License

This project is licensed under [MIT License](LICENSE).

[license-link]:  https://github.com/MarkLehoczky/gherkin-processor/blob/main/LICENSE
[release-link]:  https://github.com/MarkLehoczky/gherkin-processor/releases
[build-link]:https://github.com/MarkLehoczky/gherkin-processor/actions
[issue-link]:   https://github.com/MarkLehoczky/gherkin-processor/issues

[license-badge]: https://img.shields.io/github/license/marklehoczky/gherkin-processor?style=for-the-badge&color=success
[release-badge]: https://img.shields.io/github/v/release/marklehoczky/gherkin-processor?include_prereleases&sort=date&display_name=tag&style=for-the-badge&color=success
[build-badge]:   https://img.shields.io/github/actions/workflow/status/marklehoczky/gherkin-processor/ci.yml?style=for-the-badge
[issue-badge]:  https://img.shields.io/github/issues/marklehoczky/gherkin-processor?style=for-the-badge
[python-badge]:  https://img.shields.io/badge/Python-3.10_%7C_latest-blue?style=for-the-badge
[os-badge]:  https://img.shields.io/badge/OS-Windows_%7C_Linux_%7C_MacOS-blue?style=for-the-badge
