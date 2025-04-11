"""Provide utility functions for processing, loading, saving, and validating Gherkin files.

This module includes helper functions to process Gherkin text, load Gherkin files, save them in various formats,
and validate their syntax.
"""

from dataclasses import asdict
from json import dumps
from os import makedirs
from os.path import abspath, dirname, exists, isfile

from gherkin_processor.gherkin import Gherkin


def process(gherkin_text: str, validate_text: bool = False) -> Gherkin:
    """Process Gherkin text and return a Gherkin object.

    Args:
        gherkin_text (str): The Gherkin text to process.
        validate_text (bool): Whether to validate the syntax during processing.

    Returns:
        Gherkin: The processed Gherkin object.

    Raises:
        TypeError: If the 'text' argument is not a string.
        ValueError: If validation fails for the step syntax.
    """
    gherkin = Gherkin()
    gherkin.process(gherkin_text, validate_text)
    return gherkin


def load(file_path: str, validate_text: bool = False) -> Gherkin | None:
    """Load a Gherkin file and return a Gherkin object.

    Args:
        file_path (str): The path to the Gherkin file.
        validate_text (bool): Whether to validate the syntax during processing.

    Returns:
        Gherkin | None: The loaded Gherkin object, or None if the file does not exist.

    Raises:
        ValueError: If validation fails for the step syntax.
    """
    if file_path is not None and exists(file_path) and isfile(file_path):
        return Gherkin(file_path, validate_text)
    return None


def save(gherkin: Gherkin, file_path: str, mode: str = "GHERKIN", override_existing_file: bool = False) -> bool:
    """Save a Gherkin object to a file.

    Args:
        gherkin (Gherkin): The Gherkin object to save.
        file_path (str): The path to the output file.
        mode (str): The format to save the file in ("GHERKIN", or "JSON").
        override_existing_file (bool): Whether to override the file if it already exists.

    Returns:
        bool: True if the file was saved successfully, False otherwise.
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
    """Validate the syntax of Gherkin text.

    Args:
        gherkin_text (str): The Gherkin text to validate.

    Raises:
        TypeError: If the 'text' argument is not a string.
        ValueError: If validation fails for the step syntax.
    """
    Gherkin().process(gherkin_text, True)


def is_valid(gherkin_text: str) -> bool:
    """Check if the Gherkin text is valid.

    Args:
        gherkin_text (str): The Gherkin text to validate.

    Returns:
        bool: True if the syntax is valid, False otherwise.
    """
    try:
        Gherkin().process(gherkin_text, True)
        return True
    except (TypeError, ValueError):
        return False


def issue(gherkin_text: str) -> str:
    """Return the validation issue for Gherkin text, if any.

    Args:
        gherkin_text (str): The Gherkin text to validate.

    Returns:
        str: The validation issue as a string, or an empty string if valid.
    """
    try:
        Gherkin().process(gherkin_text, True)
        return str()
    except (TypeError, ValueError) as e:
        return str(e)
