from dataclasses import dataclass
from re import findall, split
from typing import Dict, List, Optional, Tuple


@dataclass
class Scenario:
    """Process Gherkin scenario into dataclass as parts.

    Attributes:
        tags (List[str]): Tags of the scenario. Defaults to [].
        name (str): Name / description of the scenario. Defaults to "".
        steps (List[Dict[str, Dict[str, List[str]] | str]]): Steps of the scenario. Defaults to [].
        template_table (Optional[Dict[str, List[str]]]): Template table values of the scenario. Defaults to None.
    """

    tags: List[str]
    name: str
    steps: List[Dict[str, Dict[str, List[str]] | str]]
    template_table: Optional[Dict[str, List[str]]]

    def __init__(self, scenario_text: str):
        """Process a Gherkin scenario.

        Args:
            scenario_text (str): Gherkin scenario text.
            raise_error (bool, optional): Determines error raise for invalid scenario. Defaults to True.
        """

        self.tags = []
        self.name = ""
        self.steps = []
        self.template_table = None

        self.__process(scenario_text)


    def __process(self, scenario_text: str) -> None:
        status = ""
        docstring = []
        docstring_escape = ""
        table = {}
        column = {}

        for line in scenario_text.splitlines():

            if status == "docstring" and line.strip().startswith(docstring_escape):
                self.__process_docstring_end(docstring)
                docstring = []
                status = ""
                continue
            if status == "docstring":
                docstring.append(line)
                continue
            if line.strip().startswith(('"""', "```")):
                docstring_escape = self.__process_docstring_begin(line)
                status = "docstring"
                continue

            if line.strip() != "" and not line.startswith("#"):
                line = line.strip()

            if line.startswith("@"):
                self.__process_tags(line)
            if line.startswith(("Example:", "Scenario:", "Scenario Outline:", "Scenario Template:")):
                self.__process_name(line)

            if line.startswith("|"):
                table, column = self.__process_table_row(line, table, column)
                status += "Table"
                continue
            if status.endswith("Table"):
                self.__process_table_end(status, table)
                status = ""
                table = {}
                column = {}

            if line.startswith(("Given ", "When ", "Then ", "But ", "And ", "* ")):
                self.__process_step(line)

            if line.startswith(("Examples:", "Scenarios:")):
                status = "Template"

        if status.endswith("Table"):
            self.__process_table_end(status, table)
        self.tags = list(sorted(set(self.tags)))


    def __process_tags(self, line: str) -> None:
        self.tags.extend(findall(r"@([^ ]*)", line))

    def __process_name(self, line: str) -> None:
        self.name = line.split(":", maxsplit=1)[1].lstrip()

    def __process_step(self, line: str) -> None:
        step, description = line.split(" ", maxsplit=1)
        if step in ["And", "*"]:
            step = self.steps[-1]["step"]
        self.steps.append({ "step": step, "description": description })

    def __process_docstring_begin(self, line: str) -> str:
        status = '"""' if line.strip().startswith('"""') else "```"
        docstring_language = line.strip().removeprefix(status).strip()
        if docstring_language != "":
            self.steps[-1]["docstring-language"] = docstring_language
        return status

    def __process_docstring_end(self, docstring: List[str]) -> None:
        self.steps[-1]["docstring"] = "\n".join(docstring)

    def __process_table_row(self, line: str, table: Dict[str, List[str]], column: Dict[int, str]) -> Tuple[Dict[str, List[str]], Dict[int, str]]:
        if table == {}:
            return self.__process_table_header(line)
        else:
            return self.__process_table_data(line, table, column), column

    def __process_table_header(self, line: str) -> Tuple[Dict[str, List[str]], Dict[int, str]]:
        table = {}
        columns = {}
        for index, item in enumerate(split(r"(?<!\\)(?:\\\\)*\|", line.strip('|'))):
            table[item.strip()] = []
            columns.update({ index: item.strip() })
        return table, columns

    def __process_table_data(self, line: str, table: Dict[str, List[str]], column: Dict[int, str]) -> Dict[str, List[str]]:
        for index, item in enumerate(split(r"(?<!\\)(?:\\\\)*\|", line.strip('|'))):
            table[column[index]].append(item.strip())
        return table

    def __process_table_end(self, status: str, table: Dict[str, List[str]]) -> None:
        if status.startswith("Template"):
            self.template_table = table
        else:
            self.steps[-1]["table"] = table
