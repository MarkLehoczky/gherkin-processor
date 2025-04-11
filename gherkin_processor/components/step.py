"""Define the Step class, which represents a single step in a Gherkin scenario.

The Step class provides functionality to process, validate, and convert step components into string or dictionary representations.
"""

from dataclasses import dataclass
from re import findall
from typing import Any, Dict, List, Tuple

from gherkin_processor.private.formatters import format_table


@dataclass
class Step:
    """Represent a single step in a Gherkin scenario.

    Attributes:
        type (str): The type of the step (e.g., Given, When, Then, But).
        text (str): The text of the step.
        table (Dict[str, List[str]] | None): The table associated with the step, if any.
        doc_string (str | None): The doc-string associated with the step, if any.

    Methods:
        __init__() -> None:
            Initialize the Step object with default values.
        __str__() -> str:
            Return the string representation of the Step object.
        to_string() -> str:
            Convert the Step object to a string representation.
        to_dictionary() -> Dict[str, Any]:
            Convert the Step object to a dictionary representation.
        process(text: str, validate: bool) -> bool:
            Process the step text and validate its syntax.
    """

    type: str
    text: str
    table: Dict[str, List[str]] | None
    doc_string: str | None

    def __init__(self) -> None:
        """Initialize the Step object with default values."""
        self.type = ""
        self.text = ""
        self.table = None
        self.doc_string = None

    def __str__(self) -> str:
        """Return the string representation of the Step object.

        Returns:
            str: The string representation of the Step object.
        """
        return self.to_string()

    def to_string(self) -> str:
        """Convert the Step object to a string representation.

        Returns:
            str: The string representation of the Step object.
        """
        lines: List[str] = []
        lines.append(f"{self.type} {self.text}")
        if self.table is not None:
            lines.append(format_table(self.table))
        if self.doc_string is not None:
            lines.extend(['"""', self.doc_string, '"""'])
        return "\n".join(lines)

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Step object to a dictionary representation.

        Returns:
            Dict[str, Any]: The dictionary representation of the Step object.
        """
        return {
            "type": self.type,
            "text": self.text,
            "table": self.table,
            "doc-string": self.doc_string,
        }

    def process(self, text: str, validate: bool) -> bool:
        """Process the step text and validate its syntax.

        Args:
            text (str): The step text to be processed.
            validate (bool): Whether to validate the syntax during processing.

        Returns:
            bool: True if the syntax is valid, False otherwise.

        Raises:
            TypeError: If the 'text' argument is not a string.
            ValueError: If validation fails for the step syntax.
        """
        if not isinstance(text, str):
            raise TypeError("Variable 'text' is not string type")

        valid_syntax: bool = True
        lines: List[str] = text.splitlines()
        doc_string: str = ""
        headers: List[str] = []

        for num, line in enumerate(lines, 1):
            doc_string = self._handle_docstring(doc_string, line)
            stripped_line = line.strip()

            if doc_string != "":
                if not stripped_line.startswith(("```", '"""')):
                    self.doc_string = line if self.doc_string is None else self.doc_string + "\n" + line
                continue

            valid_syntax &= self._handle_step((num, line), validate)

            if self.table is None:
                headers, is_valid = self._handle_table_header(headers, (num, line), validate)
                valid_syntax &= is_valid
            else:
                valid_syntax &= self._handle_table(headers, (num, line), validate)

        return valid_syntax

    def _handle_docstring(self, doc_string: str, text: str) -> str:
        stripped_line = text.strip()
        if stripped_line.startswith("```") and doc_string == "backquote":
            return ""
        if stripped_line.startswith("```") and doc_string == "":
            return "backquote"
        if stripped_line.startswith('"""') and doc_string == "quote":
            return ""
        if stripped_line.startswith('"""') and doc_string == "":
            return "quote"
        return doc_string

    def _handle_step(self, line: Tuple[int, str], validate: bool) -> bool:
        num, text = line
        stripped_line = text.strip()
        if stripped_line.startswith(("Given ", "When ", "Then ", "But ")):
            self.type, self.text = stripped_line.split(" ", maxsplit=1)
            if validate and not self.text:
                raise ValueError(f"Step keyword must contain text after keyword at line [{num}]: {line}")
            return bool(self.text)
        return True

    def _handle_table_header(self, headers: List[str], line: Tuple[int, str], validate: bool) -> Tuple[List[str], bool]:
        num, text = line
        stripped_line = text.strip()
        if stripped_line.startswith("|"):
            headers = [header.strip() for header in findall(r"(.+?)[^\\](?:\\\\)*\|", text)]
            headers = headers[1:]
            if validate and len(headers) <= 0:
                raise ValueError(f"Table header must contain at least one value at line [{num}]: {text}")
            self.table = {}
            for header in headers:
                self.table.update({header: []})
            return headers, bool(headers)
        return headers, True

    def _handle_table(self, headers: List[str], line: Tuple[int, str], validate: bool) -> bool:
        num, text = line
        stripped_line = text.strip()
        if stripped_line.startswith("|"):
            values = [value.strip() for value in findall(r"(.+?)[^\\](?:\\\\)*\|", text)]
            values = values[1:]

            if validate and len(values) < len(headers):
                raise ValueError(f"Table item line has less values than the table header at line [{num}]: {line}")
            if validate and len(values) > len(headers):
                raise ValueError(f"Table item line has more values than the table header at line [{num}]: {line}")
            for i in range(min(len(headers), len(values))):
                if self.table is not None:
                    self.table[headers[i]].append(values[i])
            return len(values) == len(headers)
        return True
