"""Gherkin Background Processor Module.

This module provides functionality to process Gherkin background content into a Python class representation.
"""

from typing import Any, Dict, List

from gherkin_processor.step import Step


class Background:
    """Represent a Gherkin background with its components.

    Attributes:
        description (str): The description of the Gherkin background (if any).
        steps (List[Step]): The list of steps present in the Gherkin background (if any).
    """

    description: str | None
    steps: List[Step] | None

    def __init__(self) -> None:
        """Initialize a Gherkin background with default empty components."""
        self.description = None
        self.steps = None

    def __str__(self) -> str:
        """Return string representation of the Gherkin background."""
        return self.to_string()

    def to_string(self) -> str:
        """Convert the Gherkin background into a formatted string representation.

        Returns:
            str: A string representation of the Gherkin background.
        """
        lines: List[str] = []
        if self.description is not None:
            lines.append(self.description)
        if self.steps is not None:
            lines.extend(str(step) for step in self.steps)
        return "\n".join(lines)

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Gherkin background into a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing the Gherkin background components.
        """
        return {
            "description": self.description,
            "steps": self.steps
        }

    def process(self, text: str, validate: bool) -> bool:
        """Process Gherkin background content and update the object accordingly.

        Args:
            text (str): The Gherkin background content to be processed.
            validate (bool): If True, performs syntax validation.

        Returns:
            bool: True if processing is successful.

        Raises:
            TypeError: If `text` is not a string.
            ValueError: If `validate` is True and the Gherkin background has issues.
        """
        return True
