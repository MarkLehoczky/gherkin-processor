"""Scenario class for processing Gherkin feature scenario component into python class."""

from gherkin_processor.step import Step


class Scenario:
    """Process Gherkin scenario component into python class.

    Attributes:
        tags (list[str]): List of tags associated with the scenario for categorization or filtering.
        text (list[str]): Short text that describes the scenario.
        description (list[str], optional): Free-form text of the scenario for more description.
        steps (list[str]): Ordered list of steps that define the actions within the scenario.
        outline (dict[str, list[str]], optional): Data structure representing scenario outlines with placeholders and example values.
    """

    tags: list[str]
    text: str
    description: str | None
    steps: list[Step]
    outline: dict[str, list[str]] | None

    def __init__(self, scenario_text: str = None, index: int = 0, validate: bool = False) -> None:
        """Initialize Scenario class.

        Args:
            scenario_text (str, optional): Gherkin scenario in text format. Defaults to None.
            index (int, optional): Starting index of the scenario text. Defaults to 0.
            validate (bool, optional): Determines whether to validate the scenario syntax. Defaults to False.

        Raises:
            TypeError: Variable 'scenario_text' is not string type. Only raised when validation is selected.
            ValueError: Variable 'scenario_text' has syntax or logic issue. Only raised when validation is selected.
        """
        self.tags = []
        self.text = ""
        self.description = None
        self.steps = []
        self.outline = None

        if isinstance(scenario_text, str):
            # self._process_feature(scenario_text, validate)
            pass
        elif not isinstance(scenario_text, str) and validate:
            raise TypeError("Variable 'scenario_text' must be a string")
        elif scenario_text is None and validate:
            raise ValueError("Scenario text is required when validation is selected")

    def to_dict(self, include_empty_values: bool = False) -> dict:
        return {"test": 21}

    def to_string(self, initial_indent: int = 0, indent: int = 2, alternative_step_keyword: str | None = None) -> str:
        lines = []

        lines.extend(f"@{tag}" for tag in self.tags)

        lines.append(f"{" " * initial_indent}{"Scenario Outline" if self.outline else "Scenario"}: {self.text}")
        if self.description:
            lines.append(f"{" " * initial_indent}{self.description}")

        alternative_steps = self.steps
        if alternative_step_keyword:
            for i, s in enumerate(self.steps[1:], 1):
                alternative_steps[i].keyword = s.keyword if self.steps[i-1] != s.keyword else alternative_step_keyword
        lines.extend(step.to_string(initial_indent + indent, indent) for step in alternative_steps)

        if self.outline:
            lines.append(str())
            lines.append(f"{" " * initial_indent}Scenarios:")
            lines.append(self._build_table(self.outline, initial_indent + indent))

        lines.append(str())
        return str("\n").join(lines)
