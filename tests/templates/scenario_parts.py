"""Constant scenario part file."""

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
