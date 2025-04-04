"""Gherkin Rule Processor Module.

This module provides functionality to process Gherkin rule content into a Python class representation.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Rule:
    """Represent a Gherkin rule with its components.

    Attributes:
        name (str | None): The name of the Gherkin rule (if any).
        description (str | None): The description of the Gherkin rule (if any).
    """

    name: str | None
    description: str | None

    def __init__(self) -> None:
        """Initialize a Gherkin rule with default empty components."""
        self.name = None
        self.description = None

    def __str__(self) -> str:
        """Return string representation of the Gherkin rule."""
        return self.to_string()

    def to_string(self) -> str:
        """Convert the Gherkin rule into a formatted string representation.

        Returns:
            str: A string representation of the Gherkin rule.
        """
        lines: List[str] = []
        if self.name is not None:
            lines.append(f"Rule: {self.name}")
        if self.description is not None:
            lines.append(self.description)
        return "\n".join(lines)

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Gherkin rule into a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing the Gherkin rule components.
        """
        return {
            "name": self.name,
            "description": self.description
        }

    def process(self, text: str, validate: bool) -> bool:
        """Process Gherkin rule content and update the object accordingly.

        Args:
            text (str): The Gherkin rule content to be processed.
            validate (bool): If True, performs syntax validation.

        Returns:
            bool: True if processing is successful.

        Raises:
            TypeError: If `text` is not a string.
            ValueError: If `validate` is True and the Gherkin rule has issues.
        """
        if not isinstance(text, str):
            raise TypeError("Variable 'text' is not string type")

        valid_syntax: bool = True
        status = "<BEGINNING>"
        lines: List[str] = text.splitlines()
        description: List[str] = []

        for num, line in enumerate(lines, 1):
            stripped_line = line.strip()

            if stripped_line.startswith("Rule:"):
                self.name = stripped_line.removeprefix("Rule:").lstrip()
                if validate and not self.name:
                    raise ValueError(f"Keyword 'RULE' must be followed with text at line [{num}]: {line}")
                valid_syntax = bool(self.name)
                status = "RULE"

            elif line:
                if validate and status == "<BEGINNING>":
                    raise ValueError(f"Description text cannot be before 'RULE' keyword at line [{num}]: {line}")
                valid_syntax &= status != "<BEGINNING>"
                description.append(line)

        self.description = "\n".join(description) if description else None
        return valid_syntax
