from pytest import raises
from gherkin_processor.utils import scenario
from tests.templates.scenario_parts import *


def test_no_scenario_name():
    text = (given_step
          + when_step
          + then_step)
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Prohibited keyword in '<START OF SCENARIO>' at line [1]: \"Given a activation step happens\"."
    

def test_tag_after_scenario_name():
    text = (default_scenario
          + single_tag
          + given_step
          + then_step
          + when_step)
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Prohibited keyword in 'SCENARIO name' at line [2]: \"@single\"."
    

def test_incorrect_step_order():
    text = (default_scenario
          + given_step
          + then_step
          + when_step)
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Prohibited keyword in 'GIVEN step' at line [3]: \"Then an assertion step happens\"."


def test_regular_scenario_with_template_table():
    text = (default_scenario
          + given_step
          + when_step
          + then_step
          + template_table)
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Regular SCENARIO cannot have templates at line [5]: \"Examples:\"."


def test_template_scenario_with_no_template_table():
    text = (template_scenario
          + given_step
          + when_step
          + then_step)
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "SCENARIO TEMPLATE does not have templates after '<END OF SCENARIO>' at line [4]: \"Then an assertion step happens\"."


def test_not_closed_docstring():
    text = (template_scenario
          + given_step
          + not_closed_text_docstring
          + when_step
          + then_step)
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Scenario ends in 'GIVEN step document string' at line [8]: \"Then an assertion step happens\"."
    
    
def test_header_only_table():
    text = (template_scenario
          + given_step
          + header_only_table
          + when_step
          + then_step)
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Table only has header row in 'GIVEN step table header' at line [4]: \"When an action step happens\"."
    
    
def test_table_column_misalignment():
    text = (template_scenario
          + given_step
          + not_enough_column_table
          + when_step
          + then_step)
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Incorrect table format in 'GIVEN step table' at line [5]: \"| value3 |\"."
    
    text = (template_scenario
          + given_step
          + too_many_column_table
          + when_step
          + then_step)
    with raises(ValueError) as e:
        scenario.process(text, True)
    assert str(e.value) == "Incorrect table format in 'GIVEN step table' at line [6]: \"| value5 | value6 | value7 |\"."
