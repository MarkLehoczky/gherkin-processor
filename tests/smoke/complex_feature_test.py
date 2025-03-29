from gherkin_processor.background import Background
from gherkin_processor.feature import Feature

feature_text = """Feature: Making breakfast
Describes a morning routine regarding breakfast making of an average person.

  Rule: Only one breakfast meal should be prepared
  The morning routine should include breakfast for only one person.

    Background:
    The default assumption is that every breakfast comes with coffee.
      Given I have coffee grounds
      And I add hot water
      And I get a cup of coffee

        @european
        @american @canadian
        Scenario: Making pancake
          Given I have pancake mix prepared the following way:
           \"\"\"
            Add ½ cup milk, 1 cup baking mix, 1 tbsp olive oil and 1 egg into a bowl.
            Stir the mix until the texture is consistent.
          \"\"\"
          When I cook the prepared pancake mix
          Then I get a cooked pancake
          When I top the pancake with the following ingredients:
          | ingredient  |
          | Butter      |
          | Maple syrup |
          | Blueberry   |
          Then I get an american pancake
          When I wait for the pancake to cool down
          Then the pancake is edible
          But the butter is melted

        Scenario Outline: Making eggs
        This scenario does not include all the egg making method, only selected ones.
          Given I have fresh eggs
          And I prepare the eggs by <preparing>
          When I <cook> the eggs for "<minute>" minutes
          Then I get "<name>" eggs

        Scenarios:
          | name          | preparing                        | cook  | minute |
          | Sunny side up | cracking it into a pan           | fry   | 3      |
          | Scrambled     | mixing it till consistency       | fry   | 5      |
          | Soft boiled   | placing it in boiling water      | boil  | 6      |
          | Hard boiled   | placing it in boiling water      | boil  | 12     |
          | Poached       | cracking it into simmering water | poach | 4      |
"""

def test_complex_feature_process():

    # TODO: Fix step processing
    # TODO: Implement step docstring writing
    # TODO: Fix step table processing

    feature = Feature(feature_text, True)
    assert feature.feature_text == "Making breakfast"
    assert feature.feature_description == "Describes a morning routine regarding breakfast making of an average person."
    assert feature.rule_text == "Only one breakfast meal should be prepared"
    assert feature.rule_description == "  The morning routine should include breakfast for only one person."
    assert isinstance(feature.background, Background)
    assert len(feature.scenarios) == 2

    background = feature.background
    assert background.description == "    The default assumption is that every breakfast comes with coffee."
    assert len(background.steps) == 3

    step = background.steps[0]
    assert step.keyword == "Given"
    assert step.text == "I have coffee grounds"
    assert step.argument is None
    step = background.steps[1]
    assert step.keyword == "Given"
    assert step.text == "I add hot water"
    assert step.argument is None
    step = background.steps[2]
    assert step.keyword == "Given"
    assert step.text == "I get a cup of coffee"
    assert step.argument is None

    scenario = feature.scenarios[0]
    assert scenario.tags == ["american", "canadian", "european"]
    assert scenario.text == "Making pancake"
    assert scenario.description is None
    assert len(scenario.steps) == 8
    assert scenario.outline is None

    step = scenario.steps[0]
    assert step.keyword == "Given"
    assert step.text == "I have pancake mix prepared the following way:"
    assert step.argument == {
        "doc-string": "            Add ½ cup milk, 1 cup baking mix, 1 tbsp olive oil and 1 egg into a bowl.\n            Stir the mix until the texture is consistent."
    }
    step = scenario.steps[1]
    assert step.keyword == "When"
    assert step.text == "I cook the prepared pancake mix"
    assert step.argument is None
    step = scenario.steps[2]
    assert step.keyword == "Then"
    assert step.text == "I get a cooked pancake"
    assert step.argument is None
    step = scenario.steps[3]
    assert step.keyword == "When"
    assert step.text == "I top the pancake with the following ingredients:"
    assert step.argument == {
        "ingredient": [
            "Butter",
            "Maple syrup",
            "Blueberry"
        ]
    }
    step = scenario.steps[4]
    assert step.keyword == "Then"
    assert step.text == "I get an american pancake"
    assert step.argument is None
    step = scenario.steps[5]
    assert step.keyword == "When"
    assert step.text == "I wait for the pancake to cool down"
    assert step.argument is None
    step = scenario.steps[6]
    assert step.keyword == "Then"
    assert step.text == "the pancake is edible"
    assert step.argument is None
    step = scenario.steps[7]
    assert step.keyword == "But"
    assert step.text == "the butter is melted"
    assert step.argument is None

    scenario = feature.scenarios[1]
    assert scenario.tags is None
    assert scenario.text == "Making pancake"
    assert scenario.description == "        This scenario does not include all the egg making method, only selected ones."
    assert len(scenario.steps) == 4
    assert scenario.outline == {
        "name": [
            "Sunny side up",
            "Scrambled",
            "Soft boiled",
            "Hard boiled",
            "Poached"
        ],
        "preparing": [
            "cracking it into a pan",
            "mixing it till consistency",
            "placing it in boiling water",
            "placing it in boiling water",
            "cracking it into simmering water"
        ],
        "cook": [
            "fry",
            "fry",
            "boil",
            "boil",
            "poach"

        ],
        "minute": [
            "3",
            "5",
            "6",
            "12",
            "4"
        ]
    }

    step = scenario.steps[0]
    assert step.keyword == "Given"
    assert step.text == "I have fresh eggs"
    assert step.argument is None
    step = scenario.steps[1]
    assert step.keyword == "Given"
    assert step.text == "I prepare the eggs by <preparing>"
    assert step.argument is None
    step = scenario.steps[2]
    assert step.keyword == "When"
    assert step.text == "I <cook> the eggs for \"<minute>\" minutes"
    assert step.argument is None
    step = scenario.steps[3]
    assert step.keyword == "When"
    assert step.text == "I get \"<name>\" eggs:"
    assert step.argument is None

def test_complex_feature_to_string():
    feature = Feature(feature_text)
    assert feature.to_string(indent=2, alternative_step_keyword=None) == feature_text

def test_complex_feature_to_dict():
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
