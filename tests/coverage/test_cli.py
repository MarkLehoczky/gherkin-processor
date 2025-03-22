"""Test file."""

import os


def test_save() -> None:
    os.system("python gherkin_processor/main.py -i tests/data/simple_scenario.feature -s")
    assert os.path.exists("tests/data/simple_scenario_processed.feature")
    os.remove("tests/data/simple_scenario_processed.feature")


def test_save_as_json() -> None:
    os.system("python gherkin_processor/main.py -i tests/data/simple_scenario.feature --save-as-json")
    assert os.path.exists("tests/data/simple_scenario_processed.json")
    os.remove("tests/data/simple_scenario_processed.json")
