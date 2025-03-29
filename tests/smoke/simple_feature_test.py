from gherkin_processor.feature import Feature

feature_text: str = """Feature: Making breakfast

  Scenario: Making coffee
    Given I have coffee grounds
    When I add hot water
    Then I get a cup of coffee
"""

def test_simple_feature_process():
    feature = Feature(feature_text, True)
    assert feature.feature_text == "Making breakfast"
    assert feature.feature_description is None
    assert feature.rule_text is None
    assert feature.rule_description is None
    assert feature.background is None
    assert len(feature.scenarios) == 1

    scenario = feature.scenarios[0]
    assert scenario.tags is None
    assert scenario.text == "Making coffee"
    assert scenario.description is None
    assert len(scenario.steps) == 3
    assert scenario.outline is None

    step = scenario.steps[0]
    assert step.keyword == "Given"
    assert step.text == "I have coffee grounds"
    assert step.argument is None
    step = scenario.steps[1]
    assert step.keyword == "When"
    assert step.text == "I add hot water"
    assert step.argument is None
    step = scenario.steps[2]
    assert step.keyword == "Then"
    assert step.text == "I get a cup of coffee"
    assert step.argument is None

def test_simple_feature_to_string():
    feature = Feature(feature_text)
    assert feature.to_string(indent=2, alternative_step_keyword=None) == feature_text

def test_simple_feature_to_dict():
    feature = Feature(feature_text)
    assert feature.to_dict(include_empty_values=False) == {
        "feature_text": "Making breakfast",
        "scenarios": [
            {
                "text": "Making coffee",
                "steps": [
                    {
                        "keyword": "Given",
                        "text": "I have coffee grounds"
                    },
                    {
                        "keyword": "When",
                        "text": "I add hot water"
                    },
                    {
                        "keyword": "Then",
                        "text": "I get a cup of coffee"
                    }
                ]
            }
        ]
    }
