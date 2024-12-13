"""Test file."""

from pytest import raises

from gherkin_processor.utils import scenario
from tests.templates.scenario_parts import (
    DEFAULT_SCENARIO,
    GIVEN_STEP,
    HEADER_ONLY_TABLE,
    NOT_CLOSED_TEXT_DOCSTRING,
    NOT_ENOUGH_COLUMN_TABLE,
    SINGLE_TAG,
    TEMPLATE_SCENARIO,
    TEMPLATE_TABLE,
    THEN_STEP,
    TOO_MANY_COLUMN_TABLE,
    WHEN_STEP,
)


def test_no_scenario_name() -> None:
    """Test."""
    text = GIVEN_STEP + WHEN_STEP + THEN_STEP
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Prohibited keyword in '<START OF SCENARIO>' at line [1]: \"Given a activation step happens\"."


def test_tag_after_scenario_name() -> None:
    """Test."""
    text = DEFAULT_SCENARIO + SINGLE_TAG + GIVEN_STEP + THEN_STEP + WHEN_STEP
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Prohibited keyword in 'SCENARIO name' at line [2]: \"@single\"."


def test_incorrect_step_order() -> None:
    """Test."""
    text = DEFAULT_SCENARIO + GIVEN_STEP + THEN_STEP + WHEN_STEP
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Prohibited keyword in 'GIVEN step' at line [3]: \"Then an assertion step happens\"."


def test_regular_scenario_with_template_table() -> None:
    """Test."""
    text = DEFAULT_SCENARIO + GIVEN_STEP + WHEN_STEP + THEN_STEP + TEMPLATE_TABLE
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == 'Regular SCENARIO cannot have templates at line [5]: "Examples:".'


def test_template_scenario_with_no_template_table() -> None:
    """Test."""
    text = TEMPLATE_SCENARIO + GIVEN_STEP + WHEN_STEP + THEN_STEP
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "SCENARIO TEMPLATE does not have templates after '<END OF SCENARIO>' at line [4]: \"Then an assertion step happens\"."


def test_not_closed_docstring() -> None:
    """Test."""
    text = TEMPLATE_SCENARIO + GIVEN_STEP + NOT_CLOSED_TEXT_DOCSTRING + WHEN_STEP + THEN_STEP
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Scenario ends in 'GIVEN step document string' at line [8]: \"Then an assertion step happens\"."


def test_header_only_table() -> None:
    """Test."""
    text = TEMPLATE_SCENARIO + GIVEN_STEP + HEADER_ONLY_TABLE + WHEN_STEP + THEN_STEP
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Table only has header row in 'GIVEN step table header' at line [4]: \"When an action step happens\"."


def test_table_column_misalignment() -> None:
    """Test."""
    text = TEMPLATE_SCENARIO + GIVEN_STEP + NOT_ENOUGH_COLUMN_TABLE + WHEN_STEP + THEN_STEP
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Incorrect table format in 'GIVEN step table' at line [5]: \"| value3 |\"."

    text = TEMPLATE_SCENARIO + GIVEN_STEP + TOO_MANY_COLUMN_TABLE + WHEN_STEP + THEN_STEP
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Incorrect table format in 'GIVEN step table' at line [6]: \"| value5 | value6 | value7 |\"."
