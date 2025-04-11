"""Provide the main entry point for the Gherkin processor.

This module defines the command-line interface for processing, validating, and saving Gherkin files
in various formats.
"""

import sys
from argparse import ArgumentParser, HelpFormatter, Namespace
from os.path import abspath, basename, dirname, splitext
from typing import Any

from gherkin_processor.gherkin import Gherkin
from gherkin_processor.utils import load, save


class CustomHelpFormatter(HelpFormatter):
    """Custom help formatter for the command-line interface."""

    def __init__(self, prog: Any):
        """Initialize the CustomHelpFormatter with the program name.

        Args:
            prog (Any): The program name.
        """
        super().__init__(prog, max_help_position=36)


def parse_arguments() -> Namespace:
    """Parse command-line arguments.

    Returns:
        Namespace: The parsed arguments as a Namespace object.
    """
    parser = ArgumentParser(description="Process and save Ghekin files in different formats.", formatter_class=CustomHelpFormatter)

    parser.add_argument("-i", "--input", type=str, required=True, help="input file path")
    parser.add_argument("-o", "--output", type=str, help="output file of the savings")
    parser.add_argument("-p", "--print", action="store_true", help="write the input file Gherkin syntax to standard output")
    parser.add_argument("-s", "--save", "--save-gherkin", action="store_true", help="save file as Gherkin")
    parser.add_argument("-j", "--json", "--save-json", action="store_true", help="save file as JSON")
    parser.add_argument("-y", "--yes", "--force-yes", action="store_true", help="automatically press 'y' for every user input request")
    parser.add_argument("-v", "--validate", action="store_true", help="validate the input file syntax")

    return parser.parse_args()


def save_gherkin(args: Namespace, gherkin: Gherkin) -> None:
    """Save the Gherkin object in Gherkin format.

    Args:
        args (Namespace): The command-line arguments.
        gherkin (Gherkin): The Gherkin object to save.
    """
    path = abspath(args.input)
    directory = dirname(path)
    filename, extension = splitext(basename(path))
    extension = extension.removeprefix(".")
    args.output = args.input if args.output is None else args.output
    args.output = args.output.replace("<DIR>", directory).replace("<DIRECTORY>", directory)
    args.output = args.output.replace("<NAME>", filename).replace("<FILENAME>", filename)

    defined_output = args.output.replace("<EXT>", extension).replace("<EXTENSION>", extension)
    if not save(gherkin, defined_output, "GHERKIN", False):
        if args.yes or input(f"File '{defined_output}' already exists. Would you like to replace it? [y/n] ").upper() in ["Y", "YES"]:
            save(gherkin, defined_output, "GHERKIN", True)


def save_json(args: Namespace, gherkin: Gherkin) -> None:
    """Save the Gherkin object in JSON format.

    Args:
        args (Namespace): The command-line arguments.
        gherkin (Gherkin): The Gherkin object to save.
    """
    path = abspath(args.input)
    directory = dirname(path)
    filename, extension = splitext(basename(path))
    extension = extension.removeprefix(".")
    args.output = args.input if args.output is None else args.output
    args.output = args.output.replace("<DIR>", directory).replace("<DIRECTORY>", directory)
    args.output = args.output.replace("<NAME>", filename).replace("<FILENAME>", filename)

    defined_output = args.output.replace(extension, "json").replace("<EXT>", "json").replace("<EXTENSION>", "json")
    if not save(gherkin, defined_output, "JSON", False):
        if args.yes or input(f"File '{defined_output}' already exists. Would you like to replace it? [y/n] ").upper() in ["Y", "YES"]:
            save(gherkin, defined_output, "JSON", True)


def main() -> None:
    """Run the Gherkin processor command-line interface.

    This function parses the command-line arguments, processes the input file, and performs actions
    such as saving the file in different formats, validating the syntax, or printing the Gherkin syntax.
    """
    args = parse_arguments()

    try:
        processed = load(args.input, args.validate)
    except (IOError, TypeError, ValueError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    gherkin = Gherkin() if processed is None else processed

    if args.save:
        save_gherkin(args, gherkin)

    if args.json:
        save_json(args, gherkin)

    if args.print:
        print(str(gherkin))


if __name__ == "__main__":
    main()
    sys.exit(0)
