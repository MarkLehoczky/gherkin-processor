"""Utilities Module.

This module provides high level Gherkin utilities.
"""

from dataclasses import asdict
from json import dumps
from os.path import abspath, exists

from gherkin_processor.gherkin import Gherkin


def process(gherkin_text: str, validate: bool = False) -> Gherkin:
    gherkin = Gherkin()
    gherkin.process(gherkin_text, validate)
    return gherkin


def load(file_path: str, validate: bool = False) -> Gherkin:
    return Gherkin(file_path, validate)


def save(gherkin: Gherkin, file_path: str, mode: str = "GHERKIN", override_existing_file: bool = False) -> bool:
    if not exists(abspath(file_path)):
        with open(file_path, "w", encoding="utf-8", errors="backslashreplace") as file:
            if mode in ["JSON", "JSON5"]:
                file.write(dumps(asdict(gherkin), indent=4))
            else:
                file.write(str(gherkin))
        return True
    elif override_existing_file:
        with open(file_path, "w", encoding="utf-8", errors="backslashreplace") as file:
            if mode in ["JSON", "JSON5"]:
                file.write(dumps(asdict(gherkin), indent=4))
            else:
                file.write(str(gherkin))
        return True
    return False


def validate(gherkin_text: str) -> None:
    Gherkin().process(gherkin_text, True)


def is_valid(gherkin_text: str) -> bool:
    try:
        Gherkin().process(gherkin_text, True)
        return True
    except Exception:
        return False


def issue(gherkin_text: str) -> str:
    try:
        Gherkin().process(gherkin_text, True)
        return str()
    except Exception as e:
        return str(e)
