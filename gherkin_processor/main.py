"""Main module."""

import argparse
import os
import sys

from gherkin_processor.scenario import Scenario
from gherkin_processor.utils.scenario import load, save, save_as_json


def main() -> None:
    """Entrance point for the command line interface."""
    parser = argparse.ArgumentParser(description="Gherkin Scenario processor")
    parser.add_argument("-i", "--input", type=str, required=True, help="specify the input Gherkin file location to process")
    parser.add_argument("-p", "--print", action="store_true", help="print the processed Gherkin scenario to the standard output")
    parser.add_argument("-s", "--save", action="store_true", help="save the processed Gherkin scenario to a file")
    parser.add_argument("--save-as-json", action="store_true", help="save the processed Gherkin scenario to a file in JSON format")
    parser.add_argument("--validate", action="store_true", help="validate the input Gherkin file syntax")

    args = parser.parse_args()

    try:
        path = os.path.abspath(args.input)
        directory, name = os.path.split(path)
        name, extension = os.path.splitext(name)
        scenario: Scenario = load(path, args.validate)
    except (IOError, TypeError, ValueError) as e:
        print(e, file=sys.stderr)
        return

    if args.print:
        print(str(scenario))

    if args.save:
        save(scenario, f"{directory}/{name}_processed{extension}")

    if args.save_as_json:
        save_as_json(scenario, f"{directory}/{name}_processed.json")


if __name__ == "__main__":
    main()
