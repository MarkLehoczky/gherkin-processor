import re
from typing import Dict, List


class Step:
    keyword: str
    text: str
    argument: Dict[str, List[str]] | Dict[str, str] | None

    def __init__(self, step_text: str | None = None, validate: bool = False):
        self.keyword = ""
        self.text = ""
        self.argument = None
        pass

    def add_table_line(self, num: int, line: str, validate: bool) -> bool:
        initial_argument = self.argument
        if self.argument is None or isinstance(self.argument, Dict[str, str]):
            self.argument = {}
            self._headers = re.findall(r"(?<!\\)(?:\\\\)*\|.*?(?<!\\)(?:\\\\)*\|", line)
            for header in self._headers:
                self.argument.update({ header: [] })
            return self.argument and initial_argument is None
        else:
            items = re.findall(r"(?<!\\)(?:\\\\)*\|(.*?)(?<!\\)(?:\\\\)*\|", line)
            if validate and len(items) < len(self._headers):
                raise ValueError(f"Table item line has less values than the table header at line [{num}]: {line}")
            if validate and len(items) > len(self._headers):
                raise ValueError(f"Table item line has more values than the table header at line [{num}]: {line}")
            for i in range(min(len(self._headers), len(items))):
                self.argument[self._headers[i]].append(items[i])
            return len(items) == len(self._headers)

    def add_docstring(self, line: str) -> None:
        initial_argument = self.argument
        if self.argument is None or isinstance(self.argument, Dict[str, List[str]]):
            self.argument = { "doc-string": line }
            return self.argument and initial_argument is None
        else:
            self.argument["doc-string"] += "\n" + line
            return self.argument
