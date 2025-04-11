"""Provide utility functions for formatting Gherkin components.

This module includes functions to format Gherkin components, such as tables, into string representations.
"""

from typing import Dict, List


def format_table(table: Dict[str, List[str]]) -> str:
    """Format a dictionary representing a table into a string.

    Args:
        table (Dict[str, List[str]]): A dictionary where keys are column headers and values are lists of column values.

    Returns:
        str: A formatted string representation of the table.
    """
    headers: List[str] = list(table.keys())
    values: List[List[str]] = list(table.values())

    max_column_width: List[int] = [max(len(headers[i]), *(len(row) for row in values[i])) for i in range(len(headers))]
    max_row_length: int = max(map(len, values)) if values else 0
    lines = []

    formatted_line: str = "|"
    for i, header in enumerate(headers):
        formatted_line += f" {header}{' ' * (max_column_width[i] - len(header))} |"
    lines.append(formatted_line)

    for i in range(max_row_length):
        formatted_line = "|"
        for j, value in enumerate(values):
            if len(value) > i:
                formatted_line += f" {value[i]}{' ' * (max_column_width[j] - len(value[i]))} |"
            else:
                formatted_line += f" {' ' * max_column_width[j]} |"
        lines.append(formatted_line)

    return "\n".join(lines)
