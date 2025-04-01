"""Gherkin Background Processor Module.

This module provides functionality to process Gherkin background content into a Python class representation.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from gherkin_processor.components.step import Step
from gherkin_processor.utils.private.positions import \
    ALLOWED_BACKGROUND_POSITIONS


@dataclass
class Background:
    """Represent a Gherkin background with its components.

    Attributes:
        description (str | None): The description of the Gherkin background (if any).
        steps (List[Step] | None): The list of steps present in the Gherkin background (if any).
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

            status, is_valid = self._handle_title(status, (num, line), validate)
            valid_syntax &= is_valid

            status, is_valid = self._handle_description(status, (num, line), validate)
            valid_syntax &= is_valid

            status, step, is_valid = self._handle_step(status, step, (num, line), validate)
            valid_syntax &= is_valid

            status, is_valid = self._handle_table(status, (num, line), validate)
            valid_syntax &= is_valid

            previous, step, start, is_valid = self._process_component((status, previous, step), (start, num-1), lines, validate)
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

    def _handle_title(self, status: str, line: Tuple[int, str], validate: bool) -> Tuple[str, bool]:
        _, text = line
        stripped_line = text.strip()
        if stripped_line.startswith("Background:"):
            return "BACKGROUND", self._validate_position("BACKGROUND", status, line, validate)
        return status, True

    def _handle_description(self, status: str, line: Tuple[int, str], validate: bool) -> Tuple[str, bool]:
        _, text = line
        stripped_line = text.strip()
        if stripped_line and not stripped_line.startswith(("Background:", "Given ", "And ", "* ", "|")):
            is_valid = self._validate_position("BACKGROUND DESCRIPTION", status, line, validate)
            self.description = text if self.description is None else self.description + "\n" + text
            return "BACKGROUND DESCRIPTION", is_valid
        return status, True

    def _handle_step(self, status: str, step: str, line: Tuple[int, str], validate: bool) -> Tuple[str, str, bool]:
        num, text = line
        stripped_line = text.strip()
        if validate and stripped_line.startswith(("When", "Then", "But")):
            raise ValueError(f"Keyword '{stripped_line.split(" ", maxsplit=1)[0].upper()}' cannot be in Background component at line [{num}]: {text}")
        if stripped_line.startswith("Given "):
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

    def _validate_position(self, keyword: str, status: str, line: Tuple[int, str], validate: bool) -> bool:
        num, text = line
        allowed_positions = ALLOWED_BACKGROUND_POSITIONS.get(keyword)
        if validate and allowed_positions is None:
            if keyword.endswith("TABLE"):
                raise ValueError(f"Table component cannot be after '{keyword.removesuffix(" TABLE")}' at line [{num}]: {text}")
            if keyword.endswith("DOC-STRING"):
                raise ValueError(f"Doc-string component cannot be after '{keyword.removesuffix(" DOC-STRING")}' at line [{num}]: {text}")
            raise ValueError(f"Could not resolve current status '{keyword}' as a valid possibility at line [{num}]: {text}")
        if validate and allowed_positions is not None and status not in allowed_positions:
            raise ValueError(f"Keyword '{keyword}' cannot be after '{status}' at line [{num}]: {text}")
        return allowed_positions is not None and status in allowed_positions

    def _process_component(self, status: Tuple[str, str, str], position: Tuple[int, int], lines: List[str], validate: bool) -> Tuple[str, str, int, bool]:
        current, previous, step = status
        start, end = position
        is_valid: bool = True
        if current == "GIVEN" and previous.startswith("GIVEN"):
            if self.steps is None:
                self.steps = []
            self.steps.append(Step())
            if lines[start].strip().startswith("And "):
                fixed_step = lines[start].replace("And", step.capitalize(), count=1)
                is_valid = self.steps[-1].process(("\n" * start) + fixed_step + "\n" + "\n".join(lines[start+1:end]), validate)
            elif lines[start].strip().startswith("* "):
                fixed_step = lines[start].replace("*", step.capitalize(), count=1)
                is_valid = self.steps[-1].process(("\n" * start) + fixed_step + "\n" + "\n".join(lines[start+1:end]), validate)
            else:
                is_valid = self.steps[-1].process(("\n" * start) + "\n".join(lines[start:end]), validate)
            return current, step, end, is_valid
        return current, step, start, is_valid

    def _process_last_component(self, status: Tuple[str, str], start: int, lines: List[str], validate: bool) -> bool:
        previous, step = status
        is_valid: bool = True
        if previous == "GIVEN":
            if self.steps is None:
                self.steps = []
            self.steps.append(Step())
            if lines[start].strip().startswith("And "):
                fixed_step = lines[start].replace("And", step.capitalize(), count=1)
                is_valid = self.steps[-1].process(("\n" * start) + fixed_step + "\n" + "\n".join(lines[start+1:]), validate)
            elif lines[start].strip().startswith("* "):
                fixed_step = lines[start].replace("*", step.capitalize(), count=1)
                is_valid = self.steps[-1].process(("\n" * start) + fixed_step + "\n" + "\n".join(lines[start+1:]), validate)
            else:
                is_valid = self.steps[-1].process(("\n" * start) + "\n".join(lines[start:]), validate)
        return is_valid
