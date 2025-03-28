"""Module: 'gherkin_processor/feature.py'.

This module defines the `Feature` class for parsing and processing Gherkin feature files.
A feature file contains structured text describing software behaviors in terms of scenarios.

Classes:
    - Feature: Represents a Gherkin Feature with metadata, background, and scenarios.
"""

from typing import List, Tuple

from gherkin_processor.background import Background
from gherkin_processor.scenario import Scenario


class Feature:
    """Represents a Gherkin Feature, containing metadata, background, and scenarios.

    Attributes:
        feature_text (str): The title of the feature.
        feature_description (str | None): An optional description of the feature.
        rule_text (str | None): The title of an optional rule within the feature.
        rule_description (str | None): An optional description of the rule.
        background (Background | None): An optional background section.
        scenarios (list[Scenario]): A list of scenarios in the feature.

    Methods:
        __init__(feature_text: str | None, validate: bool): Initializes a Feature instance.
        to_dict(include_empty_values: bool): Converts the feature into a dictionary format.
        to_string(indent: int, alternative_step_keyword: str | None): Returns the feature as a Gherkin-formatted string.
        __str__(): Returns the feature as a formatted string.
        process(feature_text: str, validate: bool): Processes the feature text into its components.
    """

    feature_text: str
    feature_description: str | None
    rule_text: str | None
    rule_description: str | None
    background: Background | None
    scenarios: list[Scenario]

    def __init__(self, feature_text: str | None = None, validate: bool = False):
        """Initialize a Feature instance with optional validation.

        Args:
            feature_text (str, optional): The raw feature text. Defaults to None.
            validate (bool, optional): If True, performs validation on the input text. Defaults to False.

        Raises:
            ValueError: If validation is enabled but no feature text is provided or feature text syntax is malformed.
            TypeError: If feature_text is not a string when validation is enabled.
        """
        self.feature_text = ""
        self.feature_description = None
        self.rule_text = None
        self.rule_description = None
        self.background = None
        self.scenarios = []

        if feature_text is None and validate:
            raise ValueError("Feature text is required when validation is selected")
        if not isinstance(feature_text, str) and validate:
            raise TypeError("Variable 'feature_text' is not string type")
        self.process(str(feature_text), validate)

    def to_dict(self, include_empty_values: bool = False):
        """Convert the feature into a dictionary format.

        Args:
            include_empty_values (bool, optional): Whether to include empty or None values. Defaults to False.

        Returns:
            dict: A dictionary representation of the feature.
        """
        dictionary = {}
        dictionary["feature_text"] = self.feature_text

        def add_item(key: str, value) -> None:
            if (value is not None and value != "") or include_empty_values:
                dictionary[key] = value

        add_item("feature_description", self.feature_description)
        add_item("rule_text", self.rule_text)
        add_item("rule_description", self.rule_description)
        add_item("background", self.background.to_dict(include_empty_values) if self.background else None)

        dictionary["scenarios"] = [scenario.to_dict(include_empty_values) for scenario in self.scenarios]

        return dictionary

    def to_string(self, indent: int = 2, alternative_step_keyword: str | None = None) -> str:
        """Convert the feature into a Gherkin-formatted string.

        Args:
            indent (int, optional): The indentation level for formatting. Defaults to 2.
            alternative_step_keyword (str, optional): Alternative step keywords for formatting. Defaults to None.

        Returns:
            str: The formatted feature text.
        """
        lines = []

        lines.append(f"Feature: {self.feature_text}")
        if self.feature_description:
            lines.append(self.feature_description)
        lines.append("")

        if self.rule_text:
            lines.append(f"{' ' * indent}Rule: {self.rule_text}")
        if self.rule_description:
            lines.append(self.rule_description)
        lines.append("")

        if self.background is not None:
            background_indent = indent * (2 if self.rule_text else 1)
            lines.append(self.background.to_string(background_indent, indent, alternative_step_keyword))
        lines.append("")

        scenario_indent = indent * (3 if self.background else 2 if self.rule_text else 1)
        lines.extend(scenario.to_string(scenario_indent, indent, alternative_step_keyword) for scenario in self.scenarios)

        return "\n".join(lines)

    def __str__(self) -> str:
        """Return a string representation of the feature.

        Returns:
            str: The feature as a formatted string.
        """
        return self.to_string()

    def process(self, feature_text: str, validate: bool) -> bool:
        """Process the feature text into its components.

        Args:
            feature_text (str): The raw feature text.
            validate (bool): Whether to validate the text.

        Returns:
            bool: True if processing is valid, False otherwise.

        Raises:
            ValueError: If validation is enabled and feature text syntax is malformed.
        """
        lines: List[str] = feature_text.splitlines()
        valid_processing: bool = True
        status: str = "<START OF TEXT>"
        background_content: List[Tuple[int, str]] = []
        scenario_content: List[Tuple[int, str]] = []
        num: int = 0
        line: str = ""

        def extend(initial: str | None, extended: str) -> str | None:
            if initial and extended:
                return f"{initial}\n{extended}"
            if extended:
                return extended
            return initial

        for num, line in enumerate(lines, 1):
            status, valid_keyword_position = self._validate_keyword_position(num, line, status, validate)
            valid_processing &= valid_keyword_position

            match status:
                case ("Feature description", "DOC-STRING: Feature description"):
                    self.feature_description = extend(self.feature_description, line)
                case ("Rule description", "DOC-STRING: Rule description"):
                    self.rule_description = extend(self.rule_description, line)
                case ("Background", "DOC-STRING: Background"):
                    background_content.append((num, line))
                case ("Scenario", "DOC-STRING: Scenario"):
                    scenario_content.append((num, line))
                case "Feature":
                    status = "Feature description"
                case "Rule":
                    status = "Rule description"

        valid_processing &= self._process_background(background_content, validate)
        valid_processing &= self._process_scenarios(scenario_content, validate)
        valid_processing &= self._validate_end_position(num, line, status, validate)

        return valid_processing

    def _validate_keyword_position(self, num: int, line: str, status: str, validate: bool) -> Tuple[str, bool]:
        stripped_line: str = line.strip()
        is_valid = True

        if stripped_line.startswith(("```", '"""')) and status.startswith("DOC-STRING"):
            return status[12:], is_valid
        if stripped_line.startswith(("```", '"""')):
            return f"DOC-STRING: {status}", is_valid
        if status.startswith("DOC-STRING"):
            return status, is_valid

        if stripped_line.startswith("Feature:"):
            is_valid &= self._validate_feature_position(num, line, status, validate)
            is_valid &= self._process_feature(num, line, validate)
            return "Feature", is_valid
        if stripped_line.startswith("Rule:"):
            is_valid &= self._validate_rule_position(num, line, status, validate)
            is_valid &= self._process_rule(num, line, validate)
            return "Rule", is_valid
        if stripped_line.startswith("Background:"):
            is_valid &= self._validate_background_position(num, line, status, validate)
            status = "Background"
        if stripped_line.startswith(("@", "Scenario:", "Example:", "Scenario Outline:", "Scenario Template:")):
            is_valid &= self._validate_scenario_position(num, line, status, validate)
            status = "Scenario"
        if stripped_line.startswith(("Given ", "When ", "Then ", "But ", "And")):
            is_valid &= self._validate_step_position(num, line, status, validate)

        return status, is_valid

    def _validate_feature_position(self, num: int, line: str, status: str, validate: bool) -> bool:
        prohibited: List[str] = ["Feature", "Rule", "Background", "Scenario"]
        return self._validate_position(("Feature", num, line), prohibited, status, validate)

    def _validate_rule_position(self, num: int, line: str, status: str, validate: bool) -> bool:
        prohibited: List[str] = ["<START OF TEXT>", "Rule", "Background", "Scenario"]
        return self._validate_position(("Rule", num, line), prohibited, status, validate)

    def _validate_background_position(self, num: int, line: str, status: str, validate: bool) -> bool:
        prohibited: List[str] = ["<START OF TEXT>", "Background", "Scenario"]
        return self._validate_position(("Background", num, line), prohibited, status, validate)

    def _validate_scenario_position(self, num: int, line: str, status: str, validate: bool) -> bool:
        prohibited: List[str] = ["<START OF TEXT>"]
        return self._validate_position(("Scenario", num, line), prohibited, status, validate)

    def _validate_step_position(self, num: int, line: str, status: str, validate: bool) -> bool:
        prohibited: List[str] = ["<START OF TEXT>", "Feature", "Rule"]
        return self._validate_position(("Step", num, line), prohibited, status, validate)

    def _validate_end_position(self, num: int, line: str, status: str, validate: bool) -> bool:
        prohibited: List[str] = ["<START OF TEXT>", "Feature", "Rule", "Background"]
        if validate and status in prohibited:
            raise ValueError(f"Feature text ended after one of '{", ".join(prohibited)}' components at line [{num}]: {line}")
        return status not in prohibited

    def _validate_position(self, error_message_parts: Tuple[str, int, str], prohibited: List[str], status: str, validate: bool) -> bool:
        if validate and status in prohibited:
            component, num, line = error_message_parts
            raise ValueError(f"Keyword '{component}' cannot be present after '{", ".join(prohibited)}' components at line [{num}]: {line}")
        return status not in prohibited

    def _process_feature(self, num: int, line: str, validate: bool) -> bool:
        if validate and line.strip().removeprefix("Feature:").strip() == "":
            raise ValueError(f"Feature text does not have content at line [{num}]: {line}")
        self.feature_text = line.strip().removeprefix("Feature:").strip()
        return bool(self.feature_text)

    def _process_rule(self, num: int, line: str, validate: bool) -> bool:
        if validate and line.strip().removeprefix("Rule:").strip() == "":
            raise ValueError(f"Rule text does not have content at line [{num}]: {line}")
        self.rule_text = line.strip().removeprefix("Rule:").strip()
        return bool(self.rule_text)

    def _process_background(self, background_content: List[Tuple[int, str]], validate: bool) -> bool:
        if background_content:
            self.background = Background(self._connect_lines(background_content), validate)
        return bool(self.background)

    def _process_scenarios(self, scenario_content: List[Tuple[int, str]], validate: bool) -> bool:
        if scenario_content:
            active_scenario: bool = False
            start = 0
            for i, value in enumerate(scenario_content):
                _, line = value
                if active_scenario and line.strip().startswith("@"):
                    self.scenarios.append(Scenario(self._connect_lines(scenario_content[start:i-1]), validate))
                    active_scenario = False
                    start = i
                elif active_scenario and line.strip().startswith(("Scenario:", "Example:", "Scenario Outline:", "Scenario Template:")):
                    self.scenarios.append(Scenario(self._connect_lines(scenario_content[start:i-1]), validate))
                    active_scenario = True
                    start = i
                elif line.strip().startswith(("Scenario:", "Example:", "Scenario Outline:", "Scenario Template:")):
                    active_scenario = True
            if active_scenario:
                self.scenarios.append(Scenario(self._connect_lines(scenario_content[start:]), validate))
        return bool(all(self.scenarios))

    def _connect_lines(self, content: List[Tuple[int, str]]) -> str:
        prev_num = 0
        lines = []
        for value in content:
            num, line = value
            lines.extend([""] * (num - prev_num - 1))
            lines.append(line)
            prev_num = num
        return "\n".join(lines)
