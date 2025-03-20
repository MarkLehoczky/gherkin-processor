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
CODE_DOCSTRING = '"""python\nvariable: str = "Variable"\nprint(variable + " text")\n"""\n'

TEMPLATE_TABLE = (
    "Examples:\n| Template1 | Template2 |\n| value1    | value2    |\n| value3    | value4    |\n| value5    | value6    |\n| value7    | value8    |\n"
)


NOT_CLOSED_TEXT_DOCSTRING = '"""\nThis is the first line.\nThis is the second line.\nThis is the third line.\n'

HEADER_ONLY_TABLE = "| Key1   | Key2   |\n"
NOT_ENOUGH_COLUMN_TABLE = "| Key1   | Key2   |\n| value1 | value2 |\n| value3 |\n| value5 | value6 |\n"
TOO_MANY_COLUMN_TABLE = "| Key1   | Key2   |\n| value1 | value2 |\n| value3 | value4 |\n| value5 | value6 | value7 |\n"



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
