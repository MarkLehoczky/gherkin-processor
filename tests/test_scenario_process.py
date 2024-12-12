from gherkin_processor.utils import scenario
from tests.templates.scenario_parts import *


def test_default():
    text = (single_tag
          + default_scenario
          + given_step
          + when_step
          + then_step)
    test_scenario = scenario.process(text, True)
    assert test_scenario.tags == ["single"]
    assert test_scenario.name == "Default scenario"
    assert len(test_scenario.steps) == 3
    assert test_scenario.steps[0] == { "step": "Given", "description": "a activation step happens" }
    assert test_scenario.steps[1] == { "step": "When", "description": "an action step happens" }
    assert test_scenario.steps[2] == { "step": "Then", "description": "an assertion step happens" }
    assert test_scenario.template_table is None


def test_template():
    text = (template_scenario
          + given_step
          + when_step
          + then_step
          + template_table)
    test_scenario = scenario.process(text, True)
    assert test_scenario.tags == []
    assert test_scenario.name == "Template scenario"
    assert len(test_scenario.steps) == 3
    assert test_scenario.steps[0] == { "step": "Given", "description": "a activation step happens" }
    assert test_scenario.steps[1] == { "step": "When", "description": "an action step happens" }
    assert test_scenario.steps[2] == { "step": "Then", "description": "an assertion step happens" }
    assert test_scenario.template_table == { "Template1": ["value1", "value3", "value5", "value7"], "Template2": ["value2", "value4", "value6", "value8"] }


def test_tags():
    text = (single_tag
          + multiple_tags
          + default_scenario
          + given_step
          + when_step
          + then_step)
    test_scenario = scenario.process(text, True)
    assert test_scenario.tags == ["multiple", "single", "tags"]


def test_docstring():
    text = (default_scenario
          + given_step
          + text_docstring
          + when_step
          + code_docstring
          + then_step)
    test_scenario = scenario.process(text, True)
    assert len(test_scenario.steps) == 3
    assert test_scenario.steps[0] == { "step": "Given", "description": "a activation step happens", "docstring": "This is the first line.\nThis is the second line.\nThis is the third line." }
    assert test_scenario.steps[1] == { "step": "When", "description": "an action step happens", "docstring-language": "python", "docstring": "variable: str = \"Variable\"\nprint(variable + \" text\")" }
    assert test_scenario.steps[2] == { "step": "Then", "description": "an assertion step happens" }


def test_table():
    text = (default_scenario
          + given_step
          + single_column_table
          + when_step
          + multiple_column_table
          + then_step)
    test_scenario = scenario.process(text, True)
    assert test_scenario.steps[0] == { "step": "Given", "description": "a activation step happens", "table": { "Key": ["value1", "value2", "value3"] } }
    assert test_scenario.steps[1] == { "step": "When", "description": "an action step happens", "table": {"Key1": ["value1", "value3", "value5"], "Key2": ["value2", "value4", "value6"] } }
    assert test_scenario.steps[2] == { "step": "Then", "description": "an assertion step happens" }


def test_complex():
    text = (single_tag
          + multiple_tags
          + template_scenario
          + given_step
          + single_column_table
          + given_step
          + text_docstring
          + when_step
          + then_step
          + when_step
          + code_docstring
          + then_step
          + multiple_column_table
          + template_table)
    test_scenario = scenario.process(text, True)
    assert test_scenario.tags == ["multiple", "single", "tags"]
    assert test_scenario.name == "Template scenario"
    assert len(test_scenario.steps) == 6
    assert test_scenario.steps[0] == { "step": "Given", "description": "a activation step happens", "table": { "Key": ["value1", "value2", "value3"] } }
    assert test_scenario.steps[1] == { "step": "Given", "description": "a activation step happens", "docstring": "This is the first line.\nThis is the second line.\nThis is the third line." }
    assert test_scenario.steps[2] == { "step": "When", "description": "an action step happens" }
    assert test_scenario.steps[3] == { "step": "Then", "description": "an assertion step happens" }
    assert test_scenario.steps[4] == { "step": "When", "description": "an action step happens", "docstring-language": "python", "docstring": "variable: str = \"Variable\"\nprint(variable + \" text\")" }
    assert test_scenario.steps[5] == { "step": "Then", "description": "an assertion step happens", "table": {"Key1": ["value1", "value3", "value5"], "Key2": ["value2", "value4", "value6"] } }
    assert test_scenario.template_table == { "Template1": ["value1", "value3", "value5", "value7"], "Template2": ["value2", "value4", "value6", "value8"] }
