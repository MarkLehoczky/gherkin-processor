"""Gherkin Scenario Processor Module.

This module provides functionality to process Gherkin scenario content into a Python class representation.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from gherkin_processor.components.step import Step
from gherkin_processor.utils.private.formatters import format_table
from gherkin_processor.utils.private.positions import \
    ALLOWED_SCENARIO_POSITIONS


@dataclass
class Scenario:
    """Represent a Gherkin scenario with its components.

    Attributes:
        tags (List[str] | None): The tags of the Gherkin scenario (if any).
        name (str): The name of the Gherkin scenario.
        description (str | None): The description of the Gherkin scenario (if any).
        steps (List[Step]): The list of steps present in the Gherkin scenario (if any).
        outline (Dict[str, List[str]] | None): The outline table present in the Gherkin scenario (if any).
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
        if self.outline is not None:
            lines.append(format_table(self.outline))
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
        if not isinstance(text, str):
            raise TypeError("Variable 'text' is not string type")

        valid_syntax: bool = True
        lines: List[str] = text.splitlines()
        previous: str = "<BEGINNING>"
        status: str = "<BEGINNING>"
        step: str = ""
        doc_string: str = ""
        start: int = 0
        num: int = 0

        for num, line in enumerate(lines, 1):
            status, doc_string, is_valid = self._handle_docstring(status, doc_string, (num, line), validate)
            valid_syntax &= is_valid

            if doc_string != "" or line.strip().startswith(("```", '"""')):
                continue

            status, is_valid = self._handle_tag(status, (num, line), validate)
            valid_syntax &= is_valid

            status, is_valid = self._handle_name(status, (num, line), validate)
            valid_syntax &= is_valid

            status, is_valid = self._handle_description(status, (num, line), validate)
            valid_syntax &= is_valid

            status, step, is_valid = self._handle_step(status, step, (num, line), validate)
            valid_syntax &= is_valid

            status, is_valid = self._handle_table(status, (num, line), validate)
            valid_syntax &= is_valid

            status, is_valid = self._handle_outline(status, (num, line), validate)
            valid_syntax &= is_valid

            previous, start, is_valid = self._process_component((status, previous), (start, num-1), lines, validate)
            valid_syntax &= is_valid

        if start < num:
            valid_syntax &= self._process_last_component((previous, step), start, lines, validate)
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

    def _handle_tag(self, status: str, line: Tuple[int, str], validate: bool) -> Tuple[str, bool]:
        num, text = line
        stripped_line = text.strip()
        if stripped_line.startswith("@"):
            is_valid = self._validate_position("TAG", status, line, validate)
            if validate and not all(word.startswith("@") for word in stripped_line.split(" ")):
                raise ValueError(f"Not all text is a 'TAG' at line [{num}]: {text}")
            if self.tags is None:
                self.tags = []
            self.tags.extend([tag.removeprefix("@") for tag in filter(lambda word: word.startswith("@"), stripped_line.split(" "))])
            self.tags = sorted(list(set(self.tags)))
            return "TAG", is_valid and all(word.startswith("@") for word in text.split(" "))
        return status, True

    def _handle_name(self, status: str, line: Tuple[int, str], validate: bool) -> Tuple[str, bool]:
        num, text = line
        stripped_line = text.strip()
        if stripped_line.startswith(("Scenario:", "Example:", "Scenario Outline:", "Scenario Template:", "Example Outline:", "Example Template:")):
            is_valid = self._validate_position("SCENARIO", status, line, validate)
            if stripped_line.startswith("Scenario:"):
                self.name = stripped_line.removeprefix("Scenario:").strip()
            if stripped_line.startswith("Example:"):
                self.name = stripped_line.removeprefix("Example:").strip()
            if stripped_line.startswith(("Scenario Outline:", "Example Outline:")):
                name = stripped_line.removeprefix("Scenario ").removeprefix("Example ").removeprefix("Outline:")
                self.name = name.strip()
                self.outline = {}
            if stripped_line.startswith(("Scenario Template:", "Example Template:")):
                name = stripped_line.removeprefix("Scenario ").removeprefix("Example ").removeprefix("Template:")
                self.name = name.strip()
                self.outline = {}
            if validate and not self.name:
                raise ValueError(f"Scenario keyword must contain text after keyword at line [{num}]: {line}")
            return "SCENARIO", is_valid and bool(self.name)
        return status, True

    def _handle_description(self, status: str, line: Tuple[int, str], validate: bool) -> Tuple[str, bool]:
        _, text = line
        stripped_line = text.strip()
        if stripped_line and not stripped_line.startswith(("@",
                                                           "Scenario:",
                                                           "Example:",
                                                           "Scenario Outline:",
                                                           "Scenario Template:",
                                                           "Example Outline:",
                                                           "Example Template:",
                                                           "Given ",
                                                           "When",
                                                           "Then",
                                                           "But",
                                                           "And ",
                                                           "* ",
                                                           "|",
                                                           "Scenarios:",
                                                           "Examples:")):
            is_valid = self._validate_position("SCENARIO DESCRIPTION", status, line, validate)
            self.description = text if self.description is None else self.description + "\n" + text
            return "SCENARIO DESCRIPTION", is_valid
        return status, True

    def _handle_step(self, status: str, step: str, line: Tuple[int, str], validate: bool) -> Tuple[str, str, bool]:
        _, text = line
        stripped_line = text.strip()
        if stripped_line.startswith(("Given ", "When ", "Then ", "But ")):
            keyword = stripped_line.split(" ", maxsplit=1)[0].upper()
            return keyword, keyword, self._validate_position(keyword, status, line, validate)
        if stripped_line.startswith(("And ", "* ")):
            return step, step, self._validate_position(step, status, line, validate)
        return status, step, True

    def _handle_table(self, status: str, line: Tuple[int, str], validate: bool) -> Tuple[str, bool]:
        _, text = line
        stripped_line = text.strip()
        if stripped_line.startswith("|"):
            status = f"{status} TABLE" if not status.endswith("TABLE") else status
            return status, self._validate_position(status, status, line, validate)
        return status, True

    def _handle_outline(self, status: str, line: Tuple[int, str], validate: bool) -> Tuple[str, bool]:
        num, text = line
        stripped_line = text.strip()
        if stripped_line.startswith(("Scenarios:", "Examples:")):
            is_valid = self._validate_position("OUTLINE", status, line, validate)
            if validate and self.outline is None:
                raise ValueError(f"Scenario outline must be marked in the scenario name keyword at line [{num}]: {text}")
            return "OUTLINE", is_valid
        return status, True

    def _validate_position(self, keyword: str, status: str, line: Tuple[int, str], validate: bool) -> bool:
        num, text = line
        allowed_positions = ALLOWED_SCENARIO_POSITIONS.get(keyword)
        if validate and allowed_positions is None:
            if keyword.endswith("TABLE"):
                raise ValueError(f"Table component cannot be after '{keyword.removesuffix(" TABLE")}' at line [{num}]: {text}")
            if keyword.endswith("DOC-STRING"):
                raise ValueError(f"Doc-string component cannot be after '{keyword.removesuffix(" DOC-STRING")}' at line [{num}]: {text}")
            raise ValueError(f"Could not resolve current status '{keyword}' as a valid possibility at line [{num}]: {text}")
        if validate and allowed_positions is not None and status not in allowed_positions:
            raise ValueError(f"Keyword '{keyword}' cannot be after '{status}' at line [{num}]: {text}")
        return allowed_positions is not None and status in allowed_positions

    def _process_component(self, status: Tuple[str, str], position: Tuple[int, int], lines: List[str], validate: bool) -> Tuple[str, int, bool]:
        current, previous = status
        start, end = position
        is_valid: bool = True
        if current in ["GIVEN", "WHEN", "THEN", "BUT", "OUTLINE"]:
            match previous:
                case "GIVEN" | "WHEN" | "THEN" | "BUT":
                    if any(lines[start:end]):
                        self.steps.append(Step())
                        if lines[start].strip().startswith("And "):
                            fixed_step = lines[start].replace("And", previous.capitalize(), count=1)
                            is_valid = self.steps[-1].process(("\n" * start) + fixed_step + "\n" + "\n".join(lines[start+1:end]), validate)
                        elif lines[start].strip().startswith("* "):
                            fixed_step = lines[start].replace("*", previous.capitalize(), count=1)
                            is_valid = self.steps[-1].process(("\n" * start) + fixed_step + "\n" + "\n".join(lines[start+1:end]), validate)
                        else:
                            is_valid = self.steps[-1].process(("\n" * start) + "\n".join(lines[start:end]), validate)
                case "OUTLINE":
                    table = Step()
                    table.process(("\n" * start) + "\n".join(lines[start:end]), False)
                    self.outline = table.table
            return current, end, is_valid
        return previous, start, is_valid

    def _process_last_component(self, status: Tuple[str, str], start: int, lines: List[str], validate: bool) -> bool:
        previous, step = status
        is_valid: bool = True
        match previous:
            case "GIVEN" | "WHEN" | "THEN" | "BUT":
                if any(lines[start:]):
                    self.steps.append(Step())
                    if lines[start].strip().startswith("And "):
                        fixed_step = lines[start].replace("And", step.capitalize(), count=1)
                        is_valid = self.steps[-1].process(("\n" * start) + fixed_step + "\n" + "\n".join(lines[start+1:]), validate)
                    elif lines[start].strip().startswith("* "):
                        fixed_step = lines[start].replace("*", step.capitalize(), count=1)
                        is_valid = self.steps[-1].process(("\n" * start) + fixed_step + "\n" + "\n".join(lines[start+1:]), validate)
                    else:
                        is_valid = self.steps[-1].process(("\n" * start) + "\n".join(lines[start:]), validate)
            case "OUTLINE":
                table = Step()
                table.process(("\n" * start) + "\n".join(lines[start:]), False)
                self.outline = table.table
        return is_valid
