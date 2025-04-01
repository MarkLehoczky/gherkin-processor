"""Gherkin Feature Processor Module.

This module provides functionality to process Gherkin feature content into a Python class representation.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Feature:
    """Represent a Gherkin feature with its components.

    Attributes:
        name (str | None): The name of the Gherkin feature.
        description (str | None): The description of the Gherkin feature (if any).
    """

    name: str
    description: str | None

    def __init__(self) -> None:
        """Initialize a Gherkin feature with default empty components."""
        self.name = ""
        self.description = None

    def __str__(self) -> str:
        """Return string representation of the Gherkin feature."""
        return self.to_string()

    def to_string(self) -> str:
        """Convert the Gherkin feature into a formatted string representation.

        Returns:
            str: A string representation of the Gherkin feature.
        """
        lines: List[str] = []
        lines.append(f"Feature: {self.name}")
        if self.description is not None:
            lines.append(self.description)
        return "\n".join(lines)

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Gherkin feature into a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing the Gherkin feature components.
        """
        return {
            "name": self.name,
            "description": self.description
        }

    def process(self, text: str, validate: bool) -> bool:
        """Process Gherkin feature content and update the object accordingly.

        Args:
            text (str): The Gherkin feature content to be processed.
            validate (bool): If True, performs syntax validation.

        Returns:
            bool: True if processing is successful.

        Raises:
            TypeError: If `text` is not a string.
            ValueError: If `validate` is True and the Gherkin feature has issues.
        """
        if not isinstance(text, str):
            raise TypeError("Variable 'text' is not string type")

        valid_syntax: bool = True
        status = "<BEGINNING>"
        lines: List[str] = text.splitlines()
        description: List[str] = []

        for num, line in enumerate(lines, 1):
            stripped_line = line.strip()

            if stripped_line.startswith("Feature:"):
                self.name = stripped_line.removeprefix("Feature:").lstrip()
                if validate and not self.name:
                    raise ValueError(f"Keyword 'FEATURE' must be followed with text at line [{num}]: {line}")
                valid_syntax = bool(self.name)
                status = "FEATURE"

            elif line:
                if status == "<BEGINNING>":
                    raise ValueError(f"Description text cannot be before 'FEATURE' keyword at line [{num}]: {line}")
                valid_syntax &= status != "<BEGINNING>"
                description.append(line)

        self.description = "\n".join(description) if description else None
        return valid_syntax
