from os import remove
from os.path import exists

from gherkin_processor.gherkin import Gherkin
from gherkin_processor.util import load, save


def test_save():
    gherkin = Gherkin("tests/data/complex.feature", True)

    assert save(gherkin, "tests/data/output.feature", "GHERKIN", override_existing_file=False) is True
    assert exists("tests/data/output.feature")
    assert save(gherkin, "tests/data/output.feature", "GHERKIN", override_existing_file=True) is True
    assert exists("tests/data/output.feature")
    assert save(gherkin, "tests/data/output.feature", "GHERKIN", override_existing_file=False) is False
    remove("tests/data/output.feature")

    assert save(gherkin, "tests/data/output.json", "JSON", override_existing_file=False) is True
    assert exists("tests/data/output.json")
    assert save(gherkin, "tests/data/output.json", "JSON", override_existing_file=True) is True
    assert exists("tests/data/output.json")
    assert save(gherkin, "tests/data/output.json", "JSON", override_existing_file=False) is False
    remove("tests/data/output.json")


def test_simple_load():
    gherkin = load("tests/data/complex.feature", True)
    assert gherkin is not None
