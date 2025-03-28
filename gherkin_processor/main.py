"""Main entry point for the Gherkin processor."""


import json

from gherkin_processor.feature import Feature


def main() -> None:
    """Entry point for the command line interface."""

    feature_text = """
Feature: Making breakfast
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

    feature = Feature(feature_text, True)
    feature.to_string()
    print(json.dumps(feature.to_dict(), indent=4))

    short_feature_text = """
Feature: Making breakfast

  Scenario: Making coffee
    Given I have coffee grounds
    When I add hot water
    Then I get a cup of coffee
"""

    feature = Feature(short_feature_text, True)
    print(feature.to_string())
    print()
    print()
    print()
    print()
    print(json.dumps(feature.to_dict(), indent=4))

    pass
    # """Entrance point for the command line interface."""
    # parser = argparse.ArgumentParser(description="Gherkin Scenario processor")
    # parser.add_argument("-i", "--input", type=str, required=True, help="specify the input Gherkin file location to process")
    # parser.add_argument("-p", "--print", action="store_true", help="print the processed Gherkin scenario to the standard output")
    # parser.add_argument("-s", "--save", action="store_true", help="save the processed Gherkin scenario to a file")
    # parser.add_argument("--save-as-json", action="store_true", help="save the processed Gherkin scenario to a file in JSON format")
    # parser.add_argument("--validate", action="store_true", help="validate the input Gherkin file syntax")

    # args = parser.parse_args()

    # try:
    #     path = os.path.abspath(args.input)
    #     directory, name = os.path.split(path)
    #     name, extension = os.path.splitext(name)
    #     #scenario: Scenario = load(path, args.validate)
    # except (IOError, TypeError, ValueError) as e:
    #     print(e, file=sys.stderr)
    #     return

    # if args.print:
    #    # print(str(scenario))

    # if args.save:
    #     xsave(scenario, f"{directory}/{name}_processed{extension}")

    # if args.save_as_json:
    #     save_as_json(scenario, f"{directory}/{name}_processed.json")


if __name__ == "__main__":
    main()
