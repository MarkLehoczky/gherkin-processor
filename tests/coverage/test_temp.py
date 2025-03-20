import pytest
from gherkin_processor.utils.scenario import (
    load,
    save,
    save_as_json,
    is_valid,
    issue_description,
    process,
    validate,
)
from gherkin_processor.scenario import Scenario
from unittest.mock import mock_open, patch
from json import loads

"""Test file."""

from gherkin_processor.utils import scenario




SINGLE_TAG = "@single\n"
MULTIPLE_TAGS = "@multiple @tags\n"
DEFAULT_SCENARIO = "Scenario: Default scenario\n"
TEMPLATE_SCENARIO = "Scenario Template: Template scenario\n"

GIVEN_STEP = "Given a activation step happens\n"
WHEN_STEP = "When an action step happens\n"
THEN_STEP = "Then an assertion step happens\n"
BUT_STEP = "But an assertion step does not happen\n"
AND_STEP = "And an repeated step happens\n"
ASTERISK_STEP = "* an repeated step happens\n"

SINGLE_COLUMN_TABLE = "| Key    |\n| value1 |\n| value2 |\n| value3 |\n"
MULTIPLE_COLUMN_TABLE = "| Key1   | Key2   |\n| value1 | value2 |\n| value3 | value4 |\n| value5 | value6 |\n"

TEXT_DOCSTRING = '"""\nThis is the first line.\nThis is the second line.\nThis is the third line.\n"""\n'
CODE_DOCSTRING = '```\nvariable: str = "Variable"\nprint(variable + " text")\n```\n'

TEMPLATE_TABLE = (
    "Examples:\n| Template1 | Template2 |\n| value1    | value2    |\n| value3    | value4    |\n| value5    | value6    |\n| value7    | value8    |\n"
)


NOT_CLOSED_TEXT_DOCSTRING = '"""\nThis is the first line.\nThis is the second line.\nThis is the third line.\n'

HEADER_ONLY_TABLE = "| Key1   | Key2   |\n"
NOT_ENOUGH_COLUMN_TABLE = "| Key1   | Key2   |\n| value1 | value2 |\n| value3 |\n| value5 | value6 |\n"
TOO_MANY_COLUMN_TABLE = "| Key1   | Key2   |\n| value1 | value2 |\n| value3 | value4 |\n| value5 | value6 | value7 |\n"


def test_dummy() -> None:
    """Test."""
    text = (
        SINGLE_TAG
        + MULTIPLE_TAGS
        + SINGLE_TAG
        + TEMPLATE_SCENARIO
        + GIVEN_STEP
        + SINGLE_COLUMN_TABLE
        + GIVEN_STEP
        + MULTIPLE_COLUMN_TABLE
        + GIVEN_STEP
        + TEXT_DOCSTRING
        + GIVEN_STEP
        + CODE_DOCSTRING
        + WHEN_STEP
        + SINGLE_COLUMN_TABLE
        + WHEN_STEP
        + MULTIPLE_COLUMN_TABLE
        + WHEN_STEP
        + TEXT_DOCSTRING
        + WHEN_STEP
        + CODE_DOCSTRING
        + THEN_STEP
        + SINGLE_COLUMN_TABLE
        + THEN_STEP
        + MULTIPLE_COLUMN_TABLE
        + THEN_STEP
        + TEXT_DOCSTRING
        + THEN_STEP
        + CODE_DOCSTRING
        + BUT_STEP
        + SINGLE_COLUMN_TABLE
        + BUT_STEP
        + MULTIPLE_COLUMN_TABLE
        + BUT_STEP
        + TEXT_DOCSTRING
        + BUT_STEP
        + CODE_DOCSTRING
        + TEMPLATE_TABLE
    )
    test_scenario = scenario.process(text, True)
    assert test_scenario is not None

def alt_name() -> None:
    """Test."""

    scenario.process("Scenario Outline: test", False)
    scenario.process("Scenario Template: test", False)
    scenario.process("Example: test", False)
    scenario.process("Scenario Outline: test", False)
    scenario.process("Scenario Outline: test", False)

    text = (
        + TEMPLATE_SCENARIO
        + GIVEN_STEP
        + WHEN_STEP
        + THEN_STEP
        + "Scenarios:\n"
        + SINGLE_COLUMN_TABLE
    )

    test_val = scenario.process(text, True)

    assert test_val is not None
