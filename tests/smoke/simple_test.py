from gherkin_processor.gherkin import Gherkin


def test_simple_process():
    gherkin = Gherkin("tests\data\simple.feature", True)

    assert gherkin.feature.name == "Making breakfast"
    assert gherkin.feature.description is None

    assert gherkin.rule.name is None
    assert gherkin.rule.description is None

    assert gherkin.background.description is None
    assert gherkin.background.steps is None

    assert len(gherkin.scenarios) == 1

    assert gherkin.scenarios[0].tags is None
    assert gherkin.scenarios[0].name == "Making coffee"
    assert gherkin.scenarios[0].description is None
    assert len(gherkin.scenarios[0].steps) == 3
    assert gherkin.scenarios[0].steps[0].type == "Given"
    assert gherkin.scenarios[0].steps[0].text == "I have coffee grounds"
    assert gherkin.scenarios[0].steps[0].table is None
    assert gherkin.scenarios[0].steps[0].doc_string is None
    assert gherkin.scenarios[0].steps[1].type == "When"
    assert gherkin.scenarios[0].steps[1].text == "I add hot water"
    assert gherkin.scenarios[0].steps[1].table is None
    assert gherkin.scenarios[0].steps[1].doc_string is None
    assert gherkin.scenarios[0].steps[2].type == "Then"
    assert gherkin.scenarios[0].steps[2].text == "I get a cup of coffee"
    assert gherkin.scenarios[0].steps[2].table is None
    assert gherkin.scenarios[0].steps[2].doc_string is None
    assert gherkin.scenarios[0].outline is None
