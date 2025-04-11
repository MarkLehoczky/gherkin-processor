"""Define the Rule class, which represents a Gherkin rule.

The Rule class provides functionality to process, validate, and convert rule components into string or dictionary representations.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Rule:
    """Represent a Gherkin rule.

    Attributes:
        name (str | None): The name of the rule.
        description (str | None): The description of the rule.

    Methods:
        __init__() -> None:
            Initialize the Rule object with default values.
        __str__() -> str:
            Return the string representation of the Rule object.
        to_string() -> str:
            Convert the Rule object to a string representation.
        to_dictionary() -> Dict[str, Any]:
            Convert the Rule object to a dictionary representation.
        process(text: str, validate: bool) -> bool:
            Process the rule text and validate its syntax.
    """

    name: str | None
    description: str | None

    def __init__(self) -> None:
        """Initialize the Rule object with default values."""
        self.name = None
        self.description = None

    def __str__(self) -> str:
        """Return the string representation of the Rule object.

        Returns:
            str: The string representation of the Rule object.
        """
        return self.to_string()

    def to_string(self) -> str:
        """Convert the Rule object to a string representation.

        Returns:
            str: The string representation of the Rule object.
        """
        lines: List[str] = []
        if self.name is not None:
            lines.append(f"Rule: {self.name}")
        if self.description is not None:
            lines.append(self.description)
        return "\n".join(lines)

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Rule object to a dictionary representation.

        Returns:
            Dict[str, Any]: The dictionary representation of the Rule object.
        """
        return {
            "name": self.name,
            "description": self.description
        }

    def process(self, text: str, validate: bool) -> bool:
        """Process the rule text and validate its syntax.

        Args:
            text (str): The rule text to be processed.
            validate (bool): Whether to validate the syntax during processing.

        Returns:
            bool: True if the syntax is valid, False otherwise.

        Raises:
            TypeError: If the 'text' argument is not a string.
            ValueError: If validation fails for the rule syntax.
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
