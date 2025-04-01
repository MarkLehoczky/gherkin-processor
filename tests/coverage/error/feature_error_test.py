from pytest import raises

from gherkin_processor.components.feature import Feature


def test_feature_error():
    text = "This is an invalid description position."
    feature = Feature()
    with raises(TypeError) as e:
        feature.process(None, True)
    assert str(e.value) == "Variable 'text' is not string type"
    with raises(ValueError) as e:
        feature.process(text, True)
    assert str(e.value) == "Description text cannot be before 'FEATURE' keyword at line [1]: This is an invalid description position."

def test_feature_error_suppressing():
    text = "This is an invalid description position."
    feature = Feature()
    feature.process(text, False)
    assert feature.name == ""
    assert feature.description == "This is an invalid description position."
    with raises(TypeError) as e:
        feature.process(None, False)
    assert str(e.value) == "Variable 'text' is not string type"
