"""Utilities for Gherkin scenarios."""

from dataclasses import asdict
from json import dumps
from re import findall
from typing import Tuple

try:
    from gherkin_processor.scenario import Scenario
except ImportError:
    from src.scenario import Scenario


def load(file_path: str, raise_error: bool = True) -> Scenario:
    with open(file_path, "r", encoding="utf-8", errors="backslashreplace") as file:
        return process(file.read(), raise_error)


def save(scenario: Scenario, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8", errors="backslashreplace") as file:
        file.write(str(scenario))


def save_as_json(scenario: Scenario, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8", errors="backslashreplace") as file:
        file.write(dumps(asdict(scenario), indent=4))


def is_valid(scenario_text: str) -> bool:
    """Determine a Gherkin scenario validity.

    Args:
        scenario_text (str): Gherkin scenario text.

    Returns:
        bool: True if the scenario is valid, otherwise False.
    """
    return validate(scenario_text) is None


def issue_description(scenario_text: str) -> str:
    """Describe the first Gherkin scenario validity issue.

    Args:
        scenario_text (str): Gherkin scenario text.

    Returns:
        bool: First scenario issue description.
    """
    return str(validate(scenario_text)) if not is_valid(scenario_text) else ""


def process(scenario_text: str, raise_error: bool = True) -> Scenario:
    """Process a Gherkin scenario.

    Args:
        scenario_text (str): Gherkin scenario text.
        raise_error (bool, optional): Determines error raise for invalid scenario. Defaults to True.

    Returns:
        Scenario: Processed scenario.

    Raises:
        TypeError: Parameter `scenario_text` is not string type.
        ValueError: Incorrect `scenario_text` format.
    """
    if raise_error:
        if not isinstance(scenario_text, str):
            raise TypeError("Parameter 'scenario_text' is not string type.")
        if not is_valid(scenario_text):
            raise ValueError(issue_description(scenario_text))

    return Scenario(scenario_text)


def validate(scenario_text: str, starting_position: int = 1) -> str | None:
    """Validate a Gherkin scenario.

    Args:
        scenario_text (str): Gherkin scenario text.
        starting_position (int, optional): Starting value of the lines. Defaults to 1.

    Returns:
        str | None: Issue description if the scenario is invalid, otherwise None.
    """
    status: str = "<START OF SCENARIO>"
    outline: bool = False
    docstring_escape: str = ""
    pipe_count: int = 0

    last_pos = starting_position
    last_line = scenario_text

    issue_description: str | None = None

    if scenario_text == "":
        return "Scenario is empty."

    lines = [line.strip() for line in scenario_text.splitlines() if line.strip() and not line.strip().startswith("#")]

    if lines == []:
        return "Scenario only contains empty lines or comments."

    for pos, line in enumerate(scenario_text.splitlines(), starting_position):
        if issue_description is not None:
            return issue_description

        last_pos = pos
        last_line = line
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue

        match status:
            case "<START OF SCENARIO>":
                status, issue_description, outline = __scenario_beginning(status, pos, line)
                continue

            case "SCENARIO name":
                status, issue_description = __scenario_name(status, pos, line)
                continue

            case "GIVEN step":
                status, issue_description, docstring_escape, pipe_count = __given_step(status, pos, line)
                continue

            case "WHEN step":
                status, issue_description, docstring_escape, pipe_count = __when_step(status, pos, line)
                continue

            case "THEN step":
                status, issue_description, docstring_escape, pipe_count = __then_step(status, pos, line, outline)
                continue

            case "BUT step":
                status, issue_description, docstring_escape, pipe_count = __but_step(status, pos, line, outline)
                continue

            case "GIVEN step document string" | "WHEN step document string" | "THEN step document string" | "BUT step document string":
                status, issue_description = __step_doc_string(status, pos, line, docstring_escape)
                continue

            case "GIVEN step table header" | "WHEN step table header" | "THEN step table header" | "BUT step table header":
                status, issue_description = __step_table_header(status, pos, line, pipe_count)
                continue

            case "GIVEN step table":
                status, issue_description = __given_step_table(status, pos, line, pipe_count)
                continue

            case "WHEN step table":
                status, issue_description = __when_step_table(status, pos, line, pipe_count)
                continue

            case "THEN step table":
                status, issue_description = __then_step_table(status, pos, line, pipe_count, outline)
                continue

            case "BUT step table":
                status, issue_description = __but_step_table(status, pos, line, pipe_count, outline)
                continue

            case "TEMPLATE":
                status, issue_description, pipe_count = __template(status, pos, line)
                continue

            case "TEMPLATE header" | "TEMPLATE table":
                status, issue_description = __template_table(status, pos, line, pipe_count)
                continue

    if issue_description is not None:
        pass
    elif status in [
        "<START OF SCENARIO>",
        "SCENARIO name",
        "GIVEN step",
        "WHEN step",
        "GIVEN step table header",
        "WHEN step table header",
        "THEN step table header",
        "BUT step table header",
        "GIVEN step table",
        "WHEN step table",
        "GIVEN step document string",
        "WHEN step document string",
        "THEN step document string",
        "BUT step document string",
        "TEMPLATE",
        "TEMPLATE header",
    ]:
        issue_description = f"Scenario ends in '{status}' at line [{last_pos}]: \"{last_line}\"."
    elif outline and not status.startswith("TEMPLATE"):
        issue_description = f"SCENARIO TEMPLATE does not have templates after '<END OF SCENARIO>' at line [{last_pos}]: \"{last_line}\"."
    elif outline and status == "TEMPLATE":
        issue_description = f"SCENARIO TEMPLATE does not have table after '<END OF SCENARIO>' at line [{last_pos}]: \"{last_line}\"."
    elif outline and status == "TEMPLATE header":
        issue_description = f"SCENARIO TEMPLATE table only has headers after '<END OF SCENARIO>' at line [{last_pos}]: \"{last_line}\"."

    return issue_description


def __scenario_beginning(status: str, pos: int, line: str) -> Tuple[str, str | None, bool]:
    s = status  # status
    m = None  # message
    o = False  # outline

    if not line.startswith(("@", "Scenario:", "Scenario Template:", "Scenario Outline:", "Example:")):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    if line.startswith(("Scenario:", "Scenario Template:", "Scenario Outline:", "Example:")):
        s = "SCENARIO name"
    if line.startswith(("Scenario Template:", "Scenario Outline:")):
        o = True

    return s, m, o


def __scenario_name(status: str, pos: int, line: str) -> Tuple[str, str | None]:
    s = status  # status
    m = None  # message

    if not line.startswith("Given "):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    s = "GIVEN step"

    return s, m


def __given_step(status: str, pos: int, line: str) -> Tuple[str, str | None, str, int]:
    s = status  # status
    m = None  # message
    d = ""  # docstring escape
    p = 0  # pipe count

    if not line.startswith(("Given ", "When ", "And ", "* ", '"""', "```", "|")):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    if line.startswith("When"):
        s = "WHEN step"
    if line.startswith('"""'):
        if line.removeprefix('"""') and not line.removeprefix('"""').isalpha():
            m = f'Document string opening cannot have non-alpha characters after """ in \'{status}\' at line [{pos}]: "{line}".'
        s = "GIVEN step document string"
        d = '"""'
    if line.startswith("```"):
        if line.removeprefix("```") and not line.removeprefix('"""').isalpha():
            m = f"Document string opening cannot have non-alpha characters after ``` in '{status}' at line [{pos}]: \"{line}\"."
        s = "GIVEN step document string"
        d = "```"
    if line.startswith("|"):
        s = "GIVEN step table header"
        p = len(findall(r"(?<!\\)(\|)", line))

    return s, m, d, p


def __when_step(status: str, pos: int, line: str) -> Tuple[str, str | None, str, int]:
    s = status  # status
    m = None  # message
    d = ""  # docstring escape
    p = 0  # pipe count

    if not line.startswith(("When ", "Then ", "And ", "* ", '"""', "```", "|")):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    if line.startswith("Then"):
        s = "THEN step"
    if line.startswith('"""'):
        if line.removeprefix('"""') and not line.removeprefix('"""').isalpha():
            m = f'Document string opening cannot have non-alpha characters after """ in \'{status}\' at line [{pos}]: "{line}".'
        s = "WHEN step document string"
        d = '"""'
    if line.startswith("```"):
        if line.removeprefix("```") and not line.removeprefix('"""').isalpha():
            m = f"Document string opening cannot have non-alpha characters after ``` in '{status}' at line [{pos}]: \"{line}\"."
        s = "WHEN step document string"
        d = "```"
    if line.startswith("|"):
        s = "WHEN step table header"
        p = len(findall(r"(?<!\\)(\|)", line))

    return s, m, d, p


def __then_step(status: str, pos: int, line: str, outline: bool) -> Tuple[str, str | None, str, int]:
    s = status  # status
    m = None  # message
    d = ""  # docstring escape
    p = 0  # pipe count

    if not line.startswith(
        (
            "When",
            "Then ",
            "But ",
            "And ",
            "* ",
            '"""',
            "```",
            "|",
            "Scenarios:",
            "Examples:",
        )
    ):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    if line.startswith("But"):
        s = "BUT step"
    if line.startswith('"""'):
        if line.removeprefix('"""') and not line.removeprefix('"""').isalpha():
            m = f'Document string opening cannot have non-alpha characters after """ in \'{status}\' at line [{pos}]: "{line}".'
        s = "THEN step document string"
        d = '"""'
    if line.startswith("```"):
        if line.removeprefix("```") and not line.removeprefix('"""').isalpha():
            m = f"Document string opening cannot have non-alpha characters after ``` in '{status}' at line [{pos}]: \"{line}\"."
        s = "THEN step document string"
        d = "```"
    if line.startswith("|"):
        s = "THEN step table header"
        p = len(findall(r"(?<!\\)(\|)", line))
    if line.startswith(("Scenarios:", "Examples:")):
        if not outline:
            m = f'Regular SCENARIO cannot have templates at line [{pos}]: "{line}".'
        s = "TEMPLATE"

    return s, m, d, p


def __but_step(status: str, pos: int, line: str, outline: bool) -> Tuple[str, str | None, str, int]:
    s = status  # status
    m = None  # message
    d = ""  # docstring escape
    p = 0  # pipe count

    if not line.startswith(("But ", "And ", "* ", '"""', "```", "|", "Scenarios:", "Examples:")):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    if line.startswith('"""'):
        if line.removeprefix('"""') and not line.removeprefix('"""').isalpha():
            m = f'Document string opening cannot have non-alpha characters after """ in \'{status}\' at line [{pos}]: "{line}".'
        s = "BUT step document string"
        d = '"""'
    if line.startswith("```"):
        if line.removeprefix("```") and not line.removeprefix('"""').isalpha():
            m = f"Document string opening cannot have non-alpha characters after ``` in '{status}' at line [{pos}]: \"{line}\"."
        s = "BUT step document string"
        d = "```"
    if line.startswith("|"):
        s = "BUT step table header"
        p = len(findall(r"(?<!\\)(\|)", line))
    if line.startswith(("Scenarios:", "Examples:")):
        if not outline:
            m = f'Regular SCENARIO cannot have templates at line [{pos}]: "{line}".'
        s = "TEMPLATE"

    return s, m, d, p


def __step_table_header(status: str, pos: int, line: str, pipe_count: int) -> Tuple[str, str | None]:
    s = status  # status
    m = None  # message

    if not line.startswith("|"):
        m = f"Table only has header row in '{status}' at line [{pos}]: \"{line}\"."
    elif len(findall(r"(?<!\\)(\|)", line)) != pipe_count:
        m = f"Incorrect table format in '{status}' at line [{pos}]: \"{line}\"."
    s = status.removesuffix(" header")

    return s, m


def __step_doc_string(status: str, pos: int, line: str, docstring_escape: str) -> Tuple[str, str | None]:
    s = status  # status
    m = None  # message

    if line.startswith(docstring_escape):
        if line != docstring_escape:
            m = f"Document string ending cannot have non-alpha characters after {docstring_escape} in '{status}' at line [{pos}]: \"{line}\"."
        s = status.removesuffix(" document string")

    return s, m


def __given_step_table(status: str, pos: int, line: str, pipe_count: int) -> Tuple[str, str | None]:
    s = status  # status
    m = None  # message

    if not line.startswith(("Given ", "When ", "And ", "* ", "|")):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    elif line.startswith("|") and len(findall(r"(?<!\\)(\|)", line)) != pipe_count:
        m = f"Incorrect table format in '{status}' at line [{pos}]: \"{line}\"."
    elif line.startswith(("Given", "And", "*")):
        s = "GIVEN step"
    elif line.startswith("When"):
        s = "WHEN step"

    return s, m


def __when_step_table(status: str, pos: int, line: str, pipe_count: int) -> Tuple[str, str | None]:
    s = status  # status
    m = None  # message

    if not line.startswith(("When ", "Then ", "And ", "* ", "|")):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    elif line.startswith("|") and len(findall(r"(?<!\\)(\|)", line)) != pipe_count:
        m = f"Incorrect table format in '{status}' at line [{pos}]: \"{line}\"."
    elif line.startswith(("When", "And", "*")):
        s = "WHEN step"
    elif line.startswith("Then"):
        s = "THEN step"

    return s, m


def __then_step_table(status: str, pos: int, line: str, pipe_count: int, outline: bool) -> Tuple[str, str | None]:
    s = status  # status
    m = None  # message

    if not line.startswith(("Then ", "But ", "And ", "* ", "|", "Scenarios:", "Examples:")):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    elif line.startswith("|") and len(findall(r"(?<!\\)(\|)", line)) != pipe_count:
        m = f"Incorrect table format in '{status}' at line [{pos}]: \"{line}\"."
    elif line.startswith(("Then", "And", "*")):
        s = "THEN step"
    elif line.startswith("But"):
        s = "BUT step"
    elif line.startswith(("Scenarios:", "Examples:")):
        if not outline:
            m = f'Regular SCENARIO cannot have templates at line [{pos}]: "{line}".'
        s = "TEMPLATE"

    return s, m


def __but_step_table(status: str, pos: int, line: str, pipe_count: int, outline: bool) -> Tuple[str, str | None]:
    s = status  # status
    m = None  # message

    if not line.startswith(("But ", "And ", "* ", "|", "Scenarios:", "Examples:")):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    elif line.startswith("|") and len(findall(r"(?<!\\)(\|)", line)) != pipe_count:
        m = f"Incorrect table format in '{status}' at line [{pos}]: \"{line}\"."
    elif line.startswith(("But", "And", "*")):
        s = "BUT step"
    elif line.startswith(("Scenarios:", "Examples:")):
        if not outline:
            m = f'Regular SCENARIO cannot have templates at line [{pos}]: "{line}".'
        s = "TEMPLATE"

    return s, m


def __template(status: str, pos: int, line: str) -> Tuple[str, str | None, int]:
    s = status  # status
    m = None  # message
    p = 0  # pipe count

    if not line.startswith("|"):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    p = len(findall(r"(?<!\\)(\|)", line))
    s = "TEMPLATE header"

    return s, m, p


def __template_table(status: str, pos: int, line: str, pipe_count: int) -> Tuple[str, str | None]:
    s = status  # status
    m = None  # message

    if not line.startswith("|"):
        m = f"Prohibited keyword in '{status}' at line [{pos}]: \"{line}\"."
    elif len(findall(r"(?<!\\)(\|)", line)) != pipe_count:
        m = f"Incorrect table format in '{status}' at line [{pos}]: \"{line}\"."
    s = "TEMPLATE table"

    return s, m
