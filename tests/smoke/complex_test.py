from gherkin_processor.gherkin import Gherkin


def test_complex_process():
    gherkin = Gherkin("tests\data\complex.feature", True)

    assert gherkin.feature.name == "Making breakfast"
    assert gherkin.feature.description == "Describes a morning routine regarding breakfast making of an average person."

    assert gherkin.rule.name == "Only one breakfast meal should be prepared"
    assert gherkin.rule.description == "  The morning routine should include breakfast for only one person."

    assert gherkin.background.description == "    The default assumption is that every breakfast comes with coffee."
    assert gherkin.background.steps is not None
    assert len(gherkin.background.steps) == 3
    assert gherkin.background.steps[0].type == "Given"
    assert gherkin.background.steps[0].text == "I have coffee grounds"
    assert gherkin.background.steps[0].table is None
    assert gherkin.background.steps[0].doc_string is None
    assert gherkin.background.steps[1].type == "Given"
    assert gherkin.background.steps[1].text == "I add hot water"
    assert gherkin.background.steps[1].table is None
    assert gherkin.background.steps[1].doc_string is None
    assert gherkin.background.steps[2].type == "Given"
    assert gherkin.background.steps[2].text == "I get a cup of coffee"
    assert gherkin.background.steps[2].table is None
    assert gherkin.background.steps[2].doc_string is None

    assert len(gherkin.scenarios) == 2

    assert gherkin.scenarios[0].tags == ["american", "canadian", "european"]
    assert gherkin.scenarios[0].name == "Making pancake"
    assert gherkin.scenarios[0].description is None
    assert len(gherkin.scenarios[0].steps) == 8
    assert gherkin.scenarios[0].steps[0].type == "Given"
    assert gherkin.scenarios[0].steps[0].text == "I have pancake mix prepared the following way:"
    assert gherkin.scenarios[0].steps[0].table is None
    assert gherkin.scenarios[0].steps[0].doc_string == "            Add ½ cup milk, 1 cup baking mix, 1 tbsp olive oil and 1 egg into a bowl.\n            Stir the mix until the texture is consistent."
    assert gherkin.scenarios[0].steps[1].type == "When"
    assert gherkin.scenarios[0].steps[1].text == "I cook the prepared pancake mix"
    assert gherkin.scenarios[0].steps[1].table is None
    assert gherkin.scenarios[0].steps[1].doc_string is None
    assert gherkin.scenarios[0].steps[2].type == "Then"
    assert gherkin.scenarios[0].steps[2].text == "I get a cooked pancake"
    assert gherkin.scenarios[0].steps[2].table is None
    assert gherkin.scenarios[0].steps[2].doc_string is None
    assert gherkin.scenarios[0].steps[3].type == "When"
    assert gherkin.scenarios[0].steps[3].text == "I top the pancake with the following ingredients:"
    assert gherkin.scenarios[0].steps[3].table == {
        "ingredient": [
            "Butter",
            "Maple syrup",
            "Blueberry"
          ]
    }
    assert gherkin.scenarios[0].steps[3].doc_string is None
    assert gherkin.scenarios[0].steps[4].type == "Then"
    assert gherkin.scenarios[0].steps[4].text == "I get an american pancake"
    assert gherkin.scenarios[0].steps[4].table is None
    assert gherkin.scenarios[0].steps[4].doc_string is None
    assert gherkin.scenarios[0].steps[5].type == "When"
    assert gherkin.scenarios[0].steps[5].text == "I wait for the pancake to cool down"
    assert gherkin.scenarios[0].steps[5].table is None
    assert gherkin.scenarios[0].steps[5].doc_string is None
    assert gherkin.scenarios[0].steps[6].type == "Then"
    assert gherkin.scenarios[0].steps[6].text == "the pancake is edible"
    assert gherkin.scenarios[0].steps[6].table is None
    assert gherkin.scenarios[0].steps[6].doc_string is None
    assert gherkin.scenarios[0].steps[7].type == "But"
    assert gherkin.scenarios[0].steps[7].text == "the butter is melted"
    assert gherkin.scenarios[0].steps[7].table is None
    assert gherkin.scenarios[0].steps[7].doc_string is None
    assert gherkin.scenarios[0].outline is None

    assert gherkin.scenarios[1].tags is None
    assert gherkin.scenarios[1].name == "Making eggs"
    assert gherkin.scenarios[1].description == "        This scenario does not include all the egg making method, only selected ones."
    assert len(gherkin.scenarios[1].steps) == 4
    assert gherkin.scenarios[1].steps[0].type == "Given"
    assert gherkin.scenarios[1].steps[0].text == "I have fresh eggs"
    assert gherkin.scenarios[1].steps[0].table is None
    assert gherkin.scenarios[1].steps[0].doc_string is None
    assert gherkin.scenarios[1].steps[1].type == "Given"
    assert gherkin.scenarios[1].steps[1].text == "I prepare the eggs by <preparing>"
    assert gherkin.scenarios[1].steps[1].table is None
    assert gherkin.scenarios[1].steps[1].doc_string is None
    assert gherkin.scenarios[1].steps[2].type == "When"
    assert gherkin.scenarios[1].steps[2].text == "I <cook> the eggs for \"<minute>\" minutes"
    assert gherkin.scenarios[1].steps[2].table is None
    assert gherkin.scenarios[1].steps[2].doc_string is None
    assert gherkin.scenarios[1].steps[3].type == "Then"
    assert gherkin.scenarios[1].steps[3].text == "I get \"<name>\" eggs"
    assert gherkin.scenarios[1].steps[3].table is None
    assert gherkin.scenarios[1].steps[3].doc_string is None
    temp = gherkin.scenarios[1].outline
    assert gherkin.scenarios[1].outline == {
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
