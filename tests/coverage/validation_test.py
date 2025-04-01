from pytest import raises

from gherkin_processor.util import is_valid, issue, validate


def test_is_valid():
    text = open("tests/data/simple.feature").read()
    assert is_valid(text) is True
    text = open("tests/data/invalid/missing_feature.feature").read()
    assert is_valid(text) is False


def test_issue():
    text = open("tests/data/simple.feature").read()
    assert issue(text) == ""
    text = open("tests/data/invalid/missing_feature.feature").read()
    assert issue(text) == "Keyword 'SCENARIO' cannot be after '<BEGINNING>' at line [1]: Scenario: Making coffee"


def test_validate():
    text = open("tests/data/simple.feature").read()
    assert validate(text) is None
    text = open("tests/data/invalid/missing_feature.feature").read()
    with raises(ValueError) as e:
        validate(text)
    assert str(e.value) == "Keyword 'SCENARIO' cannot be after '<BEGINNING>' at line [1]: Scenario: Making coffee"
