"""Define the Feature class, which represents a Gherkin feature.

The Feature class provides functionality to process, validate, and convert feature components into string or dictionary representations.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Feature:
    """Represent a Gherkin feature.

    Attributes:
        name (str): The name of the feature.
        description (str | None): The description of the feature.

    Methods:
        __init__() -> None:
            Initialize the Feature object with default values.
        __str__() -> str:
            Return the string representation of the Feature object.
        to_string() -> str:
            Convert the Feature object to a string representation.
        to_dictionary() -> Dict[str, Any]:
            Convert the Feature object to a dictionary representation.
        process(text: str, validate: bool) -> bool:
            Process the feature text and validate its syntax.
    """

    name: str
    description: str | None

    def __init__(self) -> None:
        """Initialize the Feature object with default values."""
        self.name = ""
        self.description = None

    def __str__(self) -> str:
        """Return the string representation of the Feature object.

        Returns:
            str: The string representation of the Feature object.
        """
        return self.to_string()

    def to_string(self) -> str:
        """Convert the Feature object to a string representation.

        Returns:
            str: The string representation of the Feature object.
        """
        lines: List[str] = []
        lines.append(f"Feature: {self.name}")
        if self.description is not None:
            lines.append(self.description)
        return "\n".join(lines)

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Feature object to a dictionary representation.

        Returns:
            Dict[str, Any]: The dictionary representation of the Feature object.
        """
        return {
            "name": self.name,
            "description": self.description
        }

    def process(self, text: str, validate: bool) -> bool:
        """Process the feature text and validate its syntax.

        Args:
            text (str): The feature text to be processed.
            validate (bool): Whether to validate the syntax during processing.

        Returns:
            bool: True if the syntax is valid, False otherwise.

        Raises:
            TypeError: If the 'text' argument is not a string.
            ValueError: If validation fails for the feature syntax.
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
                if validate and status == "<BEGINNING>":
                    raise ValueError(f"Description text cannot be before 'FEATURE' keyword at line [{num}]: {line}")
                valid_syntax &= status != "<BEGINNING>"
                description.append(line)

        self.description = "\n".join(description) if description else None
        return valid_syntax
