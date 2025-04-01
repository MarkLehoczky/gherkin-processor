from pytest import raises

from gherkin_processor.components.rule import Rule


def test_feature_error():
    text = "This is an invalid description position."
    rule = Rule()
    with raises(TypeError) as e:
        rule.process(None, True)
    assert str(e.value) == "Variable 'text' is not string type"
    with raises(ValueError) as e:
        rule.process(text, True)
    assert str(e.value) == "Description text cannot be before 'RULE' keyword at line [1]: This is an invalid description position."

def test_feature_error_suppressing():
    text = "This is an invalid description position."
    rule = Rule()
    rule.process(text, False)
    assert rule.name is None
    assert rule.description == "This is an invalid description position."
    with raises(TypeError) as e:
        rule.process(None, False)
    assert str(e.value) == "Variable 'text' is not string type"
