"""Background class for processing Gherkin feature background component into python class."""

from gherkin_processor.step import Step


class Background:
    """Process Gherkin feature background component into python class.

    Attributes:
        description (str, optional): Free-form text of the background for more description.
        steps (list[Step]): Ordered list of steps that define the actions within the background.
    """

    description: str | None
    steps: list[Step]

    def __init__(self, background_text: str = None, index: int = 0, validate: bool = False) -> None:
        self.temp = {
            "background_text": background_text,
            "index": index,
            "validate": validate
        }

    def to_dict(self, include_empty_values: bool = False) -> dict:
        self.temp["include_empty_values"] = include_empty_values
        return self.temp

    def to_string(self, initial_indent: int = 0, indent: int = 0, alternative_step_keyword: str | None = None) -> str:
        self.temp["initial_indent"] = initial_indent
        self.temp["indent"] = indent
        self.temp["alternative_step_keyword"] = alternative_step_keyword
        return str(self.temp)
