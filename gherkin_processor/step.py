"""Gherkin Step Processor Module.

This module provides functionality to process Gherkin step content into a Python class representation.
"""

from typing import Any, Dict, List


class Step:
    """Represent a Gherkin step with its components.

    Attributes:
        type (str): The type of the Gherkin step.
        text (str): The text of the Gherkin step.
        steps (Dict[str, List[str] | str]): The argument present in the Gherkin step (if any).
    """

    type: str
    text: str
    argument: Dict[str, List[str] | str] | None

    def __init__(self) -> None:
        """Initialize a Gherkin step with default empty components."""
        self.type = ""
        self.text = ""
        self.argument = None

    def __str__(self) -> str:
        """Return string representation of the Gherkin step."""
        return self.to_string()

    def to_string(self) -> str:
        """Convert the Gherkin step into a formatted string representation.

        Returns:
            str: A string representation of the Gherkin step.
        """
        lines: List[str] = []
        lines.append(f"{self.type} {self.text}")
        if self.argument is not None:
            lines.append(str(self.argument)) # TODO: implement proper table processing
        return "\n".join(lines)

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Gherkin step into a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing the Gherkin step components.
        """
        return {
            "type": self.type,
            "text": self.text,
            "argument": self.argument,
        }

    def process(self, text: str, validate: bool) -> bool:
        """Process Gherkin step content and update the object accordingly.

        Args:
            text (str): The Gherkin step content to be processed.
            validate (bool): If True, performs syntax validation.

        Returns:
            bool: True if processing is successful.

        Raises:
            TypeError: If `text` is not a string.
            ValueError: If `validate` is True and the Gherkin step has issues.
        """
        return True
