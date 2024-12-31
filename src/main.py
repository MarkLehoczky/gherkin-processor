import os

try:
    from gherkin_processor.scenario import Scenario
    from gherkin_processor.utils.scenario import load, save, save_as_json
except ImportError:
    from scenario import Scenario
    from utils.scenario import load, save, save_as_json

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Gherkin Scenario processor")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file to process")
    parser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="Sets whether the processed scenario is saved",
    )
    parser.add_argument("--save-as-json", action="store_true", help="Sets whether the processed scenario is saved as JSON")
    parser.add_argument("--validate", action="store_true", help="Sets whether the scenario processor is validated")
    parser.add_argument(
        "-p",
        "--print",
        action="store_true",
        help="Sets whether the processed scenario is printed to the standard output",
    )
    args = parser.parse_args()

    try:
        path = os.path.abspath(args.input)
        directory, name = os.path.split(path)
        name, extension = os.path.splitext(name)
        scenario: Scenario = load(path, args.validate)
    except Exception as e:
        print(f"Error: {e}")
        return

    if args.print:
        print(str(scenario))

    if args.save:
        save(scenario, f"{directory}/{name}_processed{extension}")

    if args.save_as_json:
        save_as_json(scenario, f"{directory}/{name}_processed.json")