"""Formatter Utilities Module.

This module provides functionality to format different data types.
"""
from typing import Dict, List


def format_table(table: Dict[str, List[str]]) -> str:
    """Format a table from dictionary form into a pipe string form.

    Args:
        table (Dict[str, List[str]]): Table in dictionary form.

    Returns:
        str: Table in string form.
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
