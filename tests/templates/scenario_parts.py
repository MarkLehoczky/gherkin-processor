single_tag = "@single\n"
multiple_tags = "@multiple @tags\n"
default_scenario = "Scenario: Default scenario\n"
template_scenario = "Scenario Template: Template scenario\n"

given_step = "Given a activation step happens\n"
when_step = "When an action step happens\n"
then_step = "Then an assertion step happens\n"
but_step = "But an assertion step does not happen\n"
and_step = "And an repeated step happens\n"
asterisk_step = "* an repeated step happens\n"

single_column_table = "| Key    |\n| value1 |\n| value2 |\n| value3 |\n"
multiple_column_table = "| Key1   | Key2   |\n| value1 | value2 |\n| value3 | value4 |\n| value5 | value6 |\n"

text_docstring = "\"\"\"\nThis is the first line.\nThis is the second line.\nThis is the third line.\n\"\"\"\n"
code_docstring = "\"\"\"python\nvariable: str = \"Variable\"\nprint(variable + \" text\")\n\"\"\"\n"

template_table = "Examples:\n| Template1 | Template2 |\n| value1    | value2    |\n| value3    | value4    |\n| value5    | value6    |\n| value7    | value8    |\n"


not_closed_text_docstring =  "\"\"\"\nThis is the first line.\nThis is the second line.\nThis is the third line.\n"

header_only_table = "| Key1   | Key2   |\n"
not_enough_column_table = "| Key1   | Key2   |\n| value1 | value2 |\n| value3 |\n| value5 | value6 |\n"
too_many_column_table = "| Key1   | Key2   |\n| value1 | value2 |\n| value3 | value4 |\n| value5 | value6 | value7 |\n"
