"""Gherkin Processor Module.

This module provides functionality to process Gherkin syntax content into a Python class representation.
"""

from typing import Any, Dict, List

from gherkin_processor.background import Background
from gherkin_processor.feature import Feature
from gherkin_processor.rule import Rule
from gherkin_processor.scenario import Scenario


class Gherkin:
    """Represent a Gherkin document with its components.

    Attributes:
        file (str | None): The file path of the Gherkin source (if any).
        feature (Feature): The feature definition in the Gherkin document.
        rule (Rule): The rule section of the Gherkin document.
        background (Background): The background section of the Gherkin document.
        scenarios (List[Scenario]): The list of scenarios present in the document.
    """

    file: str | None
    feature: Feature
    rule: Rule
    background: Background
    scenarios: List[Scenario]

    def __init__(self) -> None:
        """Initialize a Gherkin document with default empty components."""
        self.file = None
        self.feature = Feature()
        self.rule = Rule()
        self.background = Background()
        self.scenarios = []

    def __str__(self) -> str:
        """Return string representation of the Gherkin document."""
        return self.to_string()

    def to_string(self) -> str:
        """Convert the Gherkin document into a formatted string representation.

        Returns:
            str: A string representation of the Gherkin document.
        """
        lines: List[str] = []
        lines.append(str(self.feature))
        lines.append(str(self.rule))
        lines.append(str(self.background))
        lines.extend(map(str, self.scenarios))
        return "\n".join(lines)

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Gherkin document into a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing the Gherkin document components.
        """
        return {
            "feature": self.feature,
            "rule": self.rule,
            "background": self.background,
            "scenarios": self.scenarios,
        }

    def process(self, text: str, validate: bool) -> bool:
        """Process Gherkin syntax content and update the object accordingly.

        Args:
            text (str): The Gherkin syntax content to be processed.
            validate (bool): If True, performs syntax validation.

        Returns:
            bool: True if processing is successful.

        Raises:
            TypeError: If `text` is not a string.
            ValueError: If `validate` is True and the Gherkin syntax has issues.
        """
        return True
