"""Test file."""

try:
    from gherkin_processor.utils import scenario
except ImportError:
    from src.utils import scenario
from tests.templates.scenario_parts import (
    CODE_DOCSTRING,
    DEFAULT_SCENARIO,
    GIVEN_STEP,
    MULTIPLE_COLUMN_TABLE,
    MULTIPLE_TAGS,
    SINGLE_COLUMN_TABLE,
    SINGLE_TAG,
    TEMPLATE_SCENARIO,
    TEMPLATE_TABLE,
    TEXT_DOCSTRING,
    THEN_STEP,
    WHEN_STEP,
)


def test_default() -> None:
    """Test."""
    text = SINGLE_TAG + DEFAULT_SCENARIO + GIVEN_STEP + WHEN_STEP + THEN_STEP
    test_scenario = scenario.process(text, True)
    assert test_scenario.tags == ["single"]
    assert test_scenario.name == "Default scenario"
    assert len(test_scenario.steps) == 3
    assert test_scenario.steps[0] == {
        "step": "Given",
        "description": "a activation step happens",
    }
    assert test_scenario.steps[1] == {
        "step": "When",
        "description": "an action step happens",
    }
    assert test_scenario.steps[2] == {
        "step": "Then",
        "description": "an assertion step happens",
    }
    assert test_scenario.template_table is None


def test_template() -> None:
    """Test."""
    text = TEMPLATE_SCENARIO + GIVEN_STEP + WHEN_STEP + THEN_STEP + TEMPLATE_TABLE
    test_scenario = scenario.process(text, True)
    assert not test_scenario.tags
    assert test_scenario.name == "Template scenario"
    assert len(test_scenario.steps) == 3
    assert test_scenario.steps[0] == {
        "step": "Given",
        "description": "a activation step happens",
    }
    assert test_scenario.steps[1] == {
        "step": "When",
        "description": "an action step happens",
    }
    assert test_scenario.steps[2] == {
        "step": "Then",
        "description": "an assertion step happens",
    }
    assert test_scenario.template_table == {
        "Template1": ["value1", "value3", "value5", "value7"],
        "Template2": ["value2", "value4", "value6", "value8"],
    }


def test_tags() -> None:
    """Test."""
    text = SINGLE_TAG + MULTIPLE_TAGS + DEFAULT_SCENARIO + GIVEN_STEP + WHEN_STEP + THEN_STEP
    test_scenario = scenario.process(text, True)
    assert test_scenario.tags == ["multiple", "single", "tags"]


def test_docstring() -> None:
    """Test."""
    text = DEFAULT_SCENARIO + GIVEN_STEP + TEXT_DOCSTRING + WHEN_STEP + CODE_DOCSTRING + THEN_STEP
    test_scenario = scenario.process(text, True)
    assert len(test_scenario.steps) == 3
    assert test_scenario.steps[0] == {
        "step": "Given",
        "description": "a activation step happens",
        "docstring": "This is the first line.\nThis is the second line.\nThis is the third line.",
    }
    assert test_scenario.steps[1] == {
        "step": "When",
        "description": "an action step happens",
        "docstring-language": "python",
        "docstring": 'variable: str = "Variable"\nprint(variable + " text")',
    }
    assert test_scenario.steps[2] == {
        "step": "Then",
        "description": "an assertion step happens",
    }


def test_table() -> None:
    """Test."""
    text = DEFAULT_SCENARIO + GIVEN_STEP + SINGLE_COLUMN_TABLE + WHEN_STEP + MULTIPLE_COLUMN_TABLE + THEN_STEP
    test_scenario = scenario.process(text, True)
    assert test_scenario.steps[0] == {
        "step": "Given",
        "description": "a activation step happens",
        "table": {"Key": ["value1", "value2", "value3"]},
    }
    assert test_scenario.steps[1] == {
        "step": "When",
        "description": "an action step happens",
        "table": {
            "Key1": ["value1", "value3", "value5"],
            "Key2": ["value2", "value4", "value6"],
        },
    }
    assert test_scenario.steps[2] == {
        "step": "Then",
        "description": "an assertion step happens",
    }


def test_complex() -> None:
    """Test."""
    text = (
        SINGLE_TAG
        + MULTIPLE_TAGS
        + TEMPLATE_SCENARIO
        + GIVEN_STEP
        + SINGLE_COLUMN_TABLE
        + GIVEN_STEP
        + TEXT_DOCSTRING
        + WHEN_STEP
        + THEN_STEP
        + WHEN_STEP
        + CODE_DOCSTRING
        + THEN_STEP
        + MULTIPLE_COLUMN_TABLE
        + TEMPLATE_TABLE
    )
    test_scenario = scenario.process(text, True)
    assert test_scenario.tags == ["multiple", "single", "tags"]
    assert test_scenario.name == "Template scenario"
    assert len(test_scenario.steps) == 6
    assert test_scenario.steps[0] == {
        "step": "Given",
        "description": "a activation step happens",
        "table": {"Key": ["value1", "value2", "value3"]},
    }
    assert test_scenario.steps[1] == {
        "step": "Given",
        "description": "a activation step happens",
        "docstring": "This is the first line.\nThis is the second line.\nThis is the third line.",
    }
    assert test_scenario.steps[2] == {
        "step": "When",
        "description": "an action step happens",
    }
    assert test_scenario.steps[3] == {
        "step": "Then",
        "description": "an assertion step happens",
    }
    assert test_scenario.steps[4] == {
        "step": "When",
        "description": "an action step happens",
        "docstring-language": "python",
        "docstring": 'variable: str = "Variable"\nprint(variable + " text")',
    }
    assert test_scenario.steps[5] == {
        "step": "Then",
        "description": "an assertion step happens",
        "table": {
            "Key1": ["value1", "value3", "value5"],
            "Key2": ["value2", "value4", "value6"],
        },
    }
    assert test_scenario.template_table == {
        "Template1": ["value1", "value3", "value5", "value7"],
        "Template2": ["value2", "value4", "value6", "value8"],
    }
