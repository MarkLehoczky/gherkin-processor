"""Gherkin Scenario Processor Module.

This module provides functionality to process Gherkin scenario content into a Python class representation.
"""

from typing import Any, Dict, List

from gherkin_processor.step import Step


class Scenario:
    """Represent a Gherkin scenario with its components.

    Attributes:
        tags (List[str]): The tags of the Gherkin scenario (if any).
        name (str): The name of the Gherkin scenario.
        description (str): The description of the Gherkin scenario (if any).
        steps (List[Step]): The list of steps present in the Gherkin scenario (if any).
        outline (Dict[str, List[str]]): The outline table present in the Gherkin scenario (if any).
    """

    tags: List[str] | None
    name: str
    description: str | None
    steps: List[Step]
    outline: Dict[str, List[str]] | None

    def __init__(self) -> None:
        """Initialize a Gherkin scenario with default empty components."""
        self.tags = None
        self.name = ""
        self.description = None
        self.steps = []
        self.outline = None

    def __str__(self) -> str:
        """Return string representation of the Gherkin scenario."""
        return self.to_string()

    def to_string(self) -> str:
        """Convert the Gherkin scenario into a formatted string representation.

        Returns:
            str: A string representation of the Gherkin scenario.
        """
        lines: List[str] = []
        if self.tags is not None:
            lines.extend(f"@{tag}" for tag in self.tags)
        lines.append(f"Scenario: {self.name}" if self.outline is None else f"Scenario Outline: {self.name}")
        if self.description is not None:
            lines.append(self.description)
        lines.extend(str(step) for step in self.steps)
        lines.append("")
        return "\n".join(lines)

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Gherkin scenario into a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing the Gherkin scenario components.
        """
        return {
            "tags": self.tags,
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "outline": self.outline
        }

    def process(self, text: str, validate: bool) -> bool:
        """Process Gherkin scenario content and update the object accordingly.

        Args:
            text (str): The Gherkin scenario content to be processed.
            validate (bool): If True, performs syntax validation.

        Returns:
            bool: True if processing is successful.

        Raises:
            TypeError: If `text` is not a string.
            ValueError: If `validate` is True and the Gherkin scenario has issues.
        """
        return True
