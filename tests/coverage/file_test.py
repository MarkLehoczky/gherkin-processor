from os.path import exists

from gherkin_processor.gherkin import Gherkin
from gherkin_processor.util import load, save
from tests.decorators import after, before
from tests.functions import empty_output_directory


@before ( empty_output_directory )
@after ( empty_output_directory )
def test_save():
    gherkin = Gherkin("tests/data/complex.feature", True)

    assert save(gherkin, "tests/data/output/gherkin.feature", "GHERKIN", override_existing_file=False) is True
    assert exists("tests/data/output/gherkin.feature")
    assert save(gherkin, "tests/data/output/gherkin.feature", "GHERKIN", override_existing_file=True) is True
    assert exists("tests/data/output/gherkin.feature")
    assert save(gherkin, "tests/data/output/gherkin.feature", "GHERKIN", override_existing_file=False) is False

    assert save(gherkin, "tests/data/output/gherkin.json", "JSON", override_existing_file=False) is True
    assert exists("tests/data/output/gherkin.json")
    assert save(gherkin, "tests/data/output/gherkin.json", "JSON", override_existing_file=True) is True
    assert exists("tests/data/output/gherkin.json")
    assert save(gherkin, "tests/data/output/gherkin.json", "JSON", override_existing_file=False) is False


def test_load():
    gherkin = load("tests/data/complex.feature", True)
    assert gherkin is not None
