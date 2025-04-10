"""Utilities Module.

This module provides high-level Gherkin utilities for processing, loading, saving, and validating Gherkin text.
"""

from dataclasses import asdict
from json import dumps
from os import makedirs
from os.path import abspath, dirname, exists, isfile

from gherkin_processor.gherkin import Gherkin


def process(gherkin_text: str, validate_text: bool = False) -> Gherkin:
    """Process Gherkin text and returns a Gherkin object.

    Args:
        gherkin_text (str): The Gherkin text to process.
        validate (bool, optional): Whether to validate the text. Defaults to False.

    Returns:
        Gherkin: The processed Gherkin object.

    Raises:
        TypeError: If `text` is not a string.
        ValueError: If `validate` is True and the Gherkin syntax has issues.
    """
    gherkin = Gherkin()
    gherkin.process(gherkin_text, validate_text)
    return gherkin


def load(file_path: str, validate_text: bool = False) -> Gherkin | None:
    """Load a Gherkin file and returns a Gherkin object.

    Args:
        file_path (str): The path to the Gherkin file.
        validate (bool, optional): Whether to validate the file content. Defaults to False.

    Returns:
        Gherkin | None: The Gherkin object if the file exists and is valid, otherwise None.

    Raises:
        TypeError: If `text` is not a string.
        ValueError: If `validate` is True and the Gherkin syntax has issues.
    """
    if file_path is not None and exists(file_path) and isfile(file_path):
        return Gherkin(file_path, validate_text)
    return None


def save(gherkin: Gherkin, file_path: str, mode: str = "GHERKIN", override_existing_file: bool = False) -> bool:
    """Save a Gherkin object to a file in the specified format.

    Args:
        gherkin (Gherkin): The Gherkin object to save.
        file_path (str): The path to save the file.
        mode (str, optional): The format to save the file in ("GHERKIN", "JSON", or "JSON5"). Defaults to "GHERKIN".
        override_existing_file (bool, optional): Whether to override an existing file. Defaults to False.

    Returns:
        bool: True if the file was saved successfully, otherwise False.
    """
    if not exists(abspath(file_path)) or override_existing_file:
        output_dir = dirname(file_path)
        if not exists(output_dir):
            makedirs(output_dir)
        with open(file_path, "w", encoding="utf-8", errors="namereplace") as file:
            if mode in ["JSON", "JSON5"]:
                file.write(dumps(asdict(gherkin), indent=4))
            else:
                file.write(str(gherkin))
        return True
    return False


def validate(gherkin_text: str) -> None:
    """Validate Gherkin text by processing it with validation enabled.

    Args:
        gherkin_text (str): The Gherkin text to validate.

    Raises:
        TypeError: If `text` is not a string.
        ValueError: If `validate` is True and the Gherkin syntax has issues.
    """
    Gherkin().process(gherkin_text, True)


def is_valid(gherkin_text: str) -> bool:
    """Check if the Gherkin text is valid.

    Args:
        gherkin_text (str): The Gherkin text to validate.

    Returns:
        bool: True if the text is valid, otherwise False.
    """
    try:
        Gherkin().process(gherkin_text, True)
        return True
    except (TypeError, ValueError):
        return False


def issue(gherkin_text: str) -> str:
    """Process Gherkin text and returns any validation issues found.

    Args:
        gherkin_text (str): The Gherkin text to check for issues.

    Returns:
        str: An error message if validation fails, otherwise an empty string.
    """
    try:
        Gherkin().process(gherkin_text, True)
        return str()
    except (TypeError, ValueError) as e:
        return str(e)
