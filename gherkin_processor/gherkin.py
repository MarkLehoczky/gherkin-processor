"""Define the Gherkin class, which is responsible for parsing and processing Gherkin syntax files.

It provides functionality to validate, process, and convert Gherkin components into string or dictionary representations.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from gherkin_processor.components.background import Background
from gherkin_processor.components.feature import Feature
from gherkin_processor.components.rule import Rule
from gherkin_processor.components.scenario import Scenario
from gherkin_processor.private.positions import ALLOWED_POSITIONS


@dataclass
class Gherkin:
    """Represent a Gherkin file and its components.

    Attributes:
        file (Optional[str]): The file path of the Gherkin file being processed.
        feature (Feature): The feature component of the Gherkin file.
        rule (Rule): The rule component of the Gherkin file.
        background (Background): The background component of the Gherkin file.
        scenarios (List[Scenario]): A list of scenarios defined in the Gherkin file.

    Methods:
        __init__(file_path: Optional[str] = None, validate: bool = True):
            Initialize the Gherkin object and optionally process a file.
        __str__() -> str:
            Return the string representation of the Gherkin object.
        to_string() -> str:
            Convert the Gherkin object to a string representation.
        to_dictionary() -> Dict[str, Any]:
            Convert the Gherkin object to a dictionary representation.
        process(text: str, validate: bool) -> bool:
            Process the Gherkin text and validate its syntax.
    """

    file: Optional[str]
    feature: Feature
    rule: Rule
    background: Background
    scenarios: List[Scenario]

    def __init__(self, file_path: Optional[str] = None, validate: bool = True) -> None:
        """Initialize the Gherkin object.

        Args:
            file_path (Optional[str]): The path to the Gherkin file to be processed.
            validate (bool): Whether to validate the syntax during processing.
        """
        self.file = None
        self.feature = Feature()
        self.rule = Rule()
        self.background = Background()
        self.scenarios = []

        if file_path is not None:
            with open(file_path, "r", encoding="utf-8", errors="namereplace") as text:
                self.file = file_path
                self.process(text.read(), validate)

    def __str__(self) -> str:
        """Return the string representation of the Gherkin object.

        Returns:
            str: The string representation of the Gherkin object.
        """
        return self.to_string()

    def to_string(self) -> str:
        """Convert the Gherkin object to a string representation.

        Returns:
            str: The string representation of the Gherkin object.
        """
        lines: List[str] = []
        lines.append(str(self.feature)) if str(self.feature) else None
        lines.append(str(self.rule)) if str(self.rule) else None
        lines.append(str(self.background)) if str(self.background) else None
        lines.extend(map(str, self.scenarios))
        return "\n".join(lines)

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Gherkin object to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary containing the Gherkin components.
        """
        return {
            "feature": self.feature,
            "rule": self.rule,
            "background": self.background,
            "scenarios": self.scenarios,
        }

    def process(self, text: str, validate: bool) -> bool:
        """Process the Gherkin text and validate its syntax.

        Args:
            text (str): The Gherkin text to be processed.
            validate (bool): Whether to validate the syntax during processing.

        Returns:
            bool: True if the syntax is valid, False otherwise.

        Raises:
            TypeError: If the 'text' argument is not a string.
            ValueError: If validation fails for the step syntax.
        """
        if validate and not isinstance(text, str):
            raise TypeError("Variable 'text' is not string type")

        valid_syntax: bool = isinstance(text, str)
        lines: List[str] = text.splitlines()
        previous: str = "<BEGINNING>"
        status: str = "<BEGINNING>"
        doc_string: str = ""
        step: str = ""
        start: int = 0
        num: int = 0

        for num, line in enumerate(lines, 1):
            status, doc_string, is_valid = self._handle_docstring(status, doc_string, (num, line), validate)
            valid_syntax &= is_valid

            if doc_string != "":
                continue

            status, is_valid = self._handle_metadata(status, (num, line), validate)
            valid_syntax &= is_valid

            status, is_valid = self._handle_background(status, (num, line), validate)
            valid_syntax &= is_valid

            status, step, is_valid = self._handle_scenario(status, step, (num, line), validate)
            valid_syntax &= is_valid

            status, is_valid = self._handle_table(status, (num, line), validate)
            valid_syntax &= is_valid

            previous, start, is_valid = self._process_component((status, previous), (start, num-1), lines, validate)
            valid_syntax &= is_valid

        if start < num:
            valid_syntax &= self._process_last_component(previous, start, lines, validate)
        return valid_syntax and is_valid

    def _handle_docstring(self, status: str, doc_string: str, line: Tuple[int, str], validate: bool) -> Tuple[str, str, bool]:
        _, text = line
        stripped_line = text.strip()
        if stripped_line.startswith("```") and doc_string == "backquote":
            return status, "", True
        if stripped_line.startswith("```") and doc_string == "":
            return f"{status} DOC-STRING", "backquote", self._validate_position(f"{status} DOC-STRING", status, line, validate)
        if stripped_line.startswith('"""') and doc_string == "quote":
            return status, "", True
        if stripped_line.startswith('"""') and doc_string == "":
            return f"{status} DOC-STRING", "quote", self._validate_position(f"{status} DOC-STRING", status, line, validate)
        return status, doc_string, True

    def _handle_metadata(self, status: str, line: Tuple[int, str], validate: bool) -> Tuple[str, bool]:
        _, text = line
        stripped_line = text.strip()
        if stripped_line.startswith("Feature:"):
            return "FEATURE", self._validate_position("FEATURE", status, line, validate)
        if stripped_line.startswith("Rule:"):
            return "RULE", self._validate_position("RULE", status, line, validate)
        return status, True

    def _handle_background(self, status: str, line: Tuple[int, str], validate: bool) -> Tuple[str, bool]:
        _, text = line
        stripped_line = text.strip()
        if stripped_line.startswith("Background:"):
            return "BACKGROUND", self._validate_position("BACKGROUND", status, line, validate)
        return status, True

    def _handle_scenario(self, status: str, step: str, line: Tuple[int, str], validate: bool) -> Tuple[str, str, bool]:
        _, text = line
        stripped_line = text.strip()
        if stripped_line.startswith("@"):
            return "TAG", step, self._validate_position("TAG", status, line, validate)
        if stripped_line.startswith(("Scenario:", "Example:", "Scenario Outline:", "Scenario Template:", "Example Outline:", "Example Template:")):
            return "SCENARIO", "GIVEN", self._validate_position("SCENARIO", status, line, validate)
        if stripped_line.startswith(("Given ", "When ", "Then ", "But ")):
            step = stripped_line.split(" ", maxsplit=1)[0].upper()
            return step, step, self._validate_position(stripped_line.split(" ", maxsplit=1)[0].upper(), status, line, validate)
        if stripped_line.startswith(("And ", "* ")):
            return status.removesuffix(" TABLE").removesuffix(" DOC-STRING"), step, self._validate_position(step, status, line, validate)
        if stripped_line.startswith(("Scenarios:", "Examples:")):
            return "OUTLINE", step, True
        return status, step, True

    def _handle_table(self, status: str, line: Tuple[int, str], validate: bool) -> Tuple[str, bool]:
        _, text = line
        stripped_line = text.strip()
        if stripped_line.startswith("|"):
            status = f"{status} TABLE" if not status.endswith("TABLE") else status
            return status, self._validate_position(f"{status} TABLE" if not status.endswith("TABLE") else status, status, line, validate)
        return status, True

    def _validate_position(self, keyword: str, status: str, line: Tuple[int, str], validate: bool) -> bool:
        num, text = line
        allowed_positions = ALLOWED_POSITIONS.get(keyword)
        if validate and allowed_positions is None:
            if keyword.endswith("TABLE"):
                raise ValueError(f"Table component cannot be after '{keyword.removesuffix(' TABLE')}' at line [{num}]: {text}")
            if keyword.endswith("DOC-STRING"):
                raise ValueError(f"Doc-string component cannot be after '{keyword.removesuffix(' DOC-STRING')}' at line [{num}]: {text}")
            raise ValueError(f"Could not resolve current status '{keyword}' as a valid possibility at line [{num}]: {text}")
        if validate and allowed_positions is not None and status not in allowed_positions:
            raise ValueError(f"Keyword '{keyword}' cannot be after '{status}' at line [{num}]: {text}")
        return allowed_positions is not None and status in allowed_positions

    def _process_component(self, status: Tuple[str, str], position: Tuple[int, int], lines: List[str], validate: bool) -> Tuple[str, int, bool]:
        current, previous = status
        start, end = position
        is_valid: bool = True
        if current in ["FEATURE", "RULE", "BACKGROUND", "TAG", "SCENARIO"] and current != previous:
            match previous:
                case "FEATURE":
                    is_valid = self.feature.process(("\n" * start) + "\n".join(lines[start:end]), validate)
                case "RULE":
                    is_valid = self.rule.process(("\n" * start) + "\n".join(lines[start:end]), validate)
                case "BACKGROUND":
                    is_valid = self.background.process(("\n" * start) + "\n".join(lines[start:end]), validate)
                case "SCENARIO":
                    self.scenarios.append(Scenario())
                    is_valid = self.scenarios[-1].process(("\n" * start) + "\n".join(lines[start:end]), validate)
                case _:
                    return current, start, is_valid
            return current, end, is_valid
        if (current == "SCENARIO" and any(line.strip().startswith((
            "Scenario:",
            "Example:",
            "Scenario Outline:",
            "Scenario Template:",
            "Example Outline:",
            "Example Template:"
        )) for line in lines[start:end-1])):
            self.scenarios.append(Scenario())
            is_valid = self.scenarios[-1].process(("\n" * start) + "\n".join(lines[start:end]), validate)
            return current, end, is_valid
        return previous, start, is_valid

    def _process_last_component(self, previous: str, start: int, lines: List[str], validate: bool) -> bool:
        is_valid: bool = True
        match previous:
            case "FEATURE":
                is_valid = self.feature.process(("\n" * start) + "\n".join(lines[start:]), validate)
            case "RULE":
                is_valid = self.rule.process(("\n" * start) + "\n".join(lines[start:]), validate)
            case "BACKGROUND":
                is_valid = self.background.process(("\n" * start) + "\n".join(lines[start:]), validate)
            case "TAG":
                self.scenarios.append(Scenario())
                is_valid = self.scenarios[-1].process(("\n" * start) + "\n".join(lines[start:]), validate)
            case "SCENARIO":
                self.scenarios.append(Scenario())
                is_valid = self.scenarios[-1].process(("\n" * start) + "\n".join(lines[start:]), validate)
        return is_valid
