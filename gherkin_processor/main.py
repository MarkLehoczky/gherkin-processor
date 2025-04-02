"""Main Entry Point.

This module serves as the main entry point for the command-line interface (CLI)
component of the project. It initializes and executes the necessary functionality
when run as a standalone script.
"""


from argparse import ArgumentParser
from os.path import abspath, basename, dirname, splitext
from sys import stderr

from gherkin_processor.util import load, save


def main() -> None:
    """Execute the CLI component."""
    parser = ArgumentParser(description="Process and save files in different formats.")

    parser.add_argument("-i", "--input", type=str, required=True, help="input file path")
    parser.add_argument("-o", "--output", type=str, help="output file of the savings")
    parser.add_argument("-p", "--print", action="store_true", help="write the input file Gherkin syntax to standard output")
    parser.add_argument("-s", "--save", "--save-as-gherkin", action="store_true", help="save file as Gherkin")
    parser.add_argument("-j", "--json", "--save-as-json", action="store_true", help="save file as JSON")
    parser.add_argument("-y", "--yes", action="store_true", help="automatically press 'y' for every user input request")
    parser.add_argument("--validate", action="store_true", help="validate the input file syntax")

    args = parser.parse_args()

    path = abspath(args.input)
    dir = dirname(path)
    filename, extension = splitext(basename(path))
    args.output = args.input if args.output is None else args.output
    args.output = args.output.replace("<DIR>", dir).replace("<DIRECTORY>", dir)
    args.output = args.output.replace("<NAME>", filename).replace("<FILENAME>", filename)

    try:
        gherkin = load(args.input, args.validate)
    except (IOError, TypeError, ValueError) as e:
        print(e, file=stderr)
        return

    if args.save:
        defined_output = args.output.replace("<EXT>", extension).replace("<EXTENSION>", extension)
        if not save(gherkin, defined_output, "GHERKIN", False):
            if args.yes or input(f"File '{defined_output}' already exists. Would you like to replace it? [y/n] ").upper() in ["Y", "YES"]:
                save(gherkin, defined_output, "GHERKIN", True)

    if args.json:
        defined_output = args.output.replace(extension, ".json").replace("<EXT>", ".json").replace("<EXTENSION>", ".json")
        if not save(gherkin, defined_output, "JSON", False):
            if args.yes or input(f"File '{defined_output}' already exists. Would you like to replace it? [y/n] ").upper() in ["Y", "YES"]:
                save(gherkin, defined_output, "JSON", True)

    if args.print:
        print(str(gherkin))

if __name__ == "__main__":
    main()
