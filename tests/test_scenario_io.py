"""Test file."""

try:
    from gherkin_processor.utils import scenario
except ImportError:
    from src.utils import scenario
import json
from pytest import raises


def test_load() -> None:
    expected_scenario = scenario.process(
        """Scenario: Make hotdog
    Given the sausage is cooked
    When the sausage is put into a bun
    Then the hotdog is ready to eat
    """
    )
    actual_scenario = scenario.load("tests/data/simple_scenario.feature")
    assert actual_scenario == expected_scenario

    with raises(ValueError) as e:
        scenario.load("tests/data/invalid_step_order_scenario.feature")
    assert str(e.value) == "Prohibited keyword in 'GIVEN step table' at line [7]: \"Then the <Type> pizza is ready to eat\"."

    with raises(ValueError) as e:
        scenario.load("tests/data/invalid_table_scenario.feature")
    assert str(e.value) == "Incorrect table format in 'GIVEN step table header' at line [5]: \"| <Sauce>    | Olive oil |\"."


def test_save_scenario() -> None:
    """Test."""
    scenario.save(scenario.load("tests/data/complex_scenario.feature"), "tests/data/saved_scenario.feature")
    with open("tests/data/saved_scenario.feature", "r", encoding="utf-8") as saved_scenario:
        assert (
            saved_scenario.read()
            == '@american\n@canadian\n@italian\nScenario Template: Make pizza\nGiven we knead the dough into a <Size> wide pizza disc\n"""markdown\n# Pizza Dough Recipe\n\n> Source: [Sam Merritt - The Best Pizza Dough Recipe (article)](https://sugarspunrun.com/the-best-pizza-dough-recipe/)\n\n## Ingredients\n\n- [ ] 2-2 ⅓ cups all-purpose flour OR bread flour divided (250-295g)\n- [ ] 1 packet instant yeast (2 ¼ teaspoon)\n- [ ] 1 ½ teaspoons sugar\n- [ ] ¾ teaspoon salt\n- [ ] ⅛-¼ teaspoon garlic powder and/or dried basil leaves optional\n- [ ] 2 Tablespoons olive oil + additional\n- [ ] ¾ cup warm water (175ml)\n\n## Instructions\n\n1. Combine 1 cup (125g) of flour, instant yeast, sugar, and salt in a large bowl. If desired, add garlic powder and dried basil at this point as well.\n2. Add olive oil and warm water and use a wooden spoon to stir well very well.\n3. Gradually add another 1 cup (125g) of flour. Add any additional flour as needed (I\'ve found that sometimes I need as much as an additional ⅓ cup), stirring until the dough is forming into a cohesive, elastic ball and is beginning to pull away from the sides of the bowl (see video above recipe for visual cue). The dough will still be slightly sticky but still should be manageable with your hands.\n4. Drizzle a separate, large, clean bowl generously with olive oil and use a pastry brush to brush up the sides of the bowl.\n5. Lightly dust your hands with flour and form your pizza dough into a round ball and transfer to your olive oil-brushed bowl. Use your hands to roll the pizza dough along the inside of the bowl until it is coated in olive oil, then cover the bowl tightly with plastic wrap and place it in a warm place.\n6. Allow dough to rise for 30 minutes or until doubled in size. If you intend to bake this dough into a pizza, I also recommend preheating your oven to 425F (215C) at this point so that it will have reached temperature once your pizza is ready to bake.\n7. Once the dough has risen, use your hands to gently deflate it and transfer to a lightly floured surface and knead briefly until smooth (about 3-5 times).\n8. Use either your hands or a rolling pin to work the dough into 12" circle.\n9. Transfer dough to a parchment paper lined pizza pan and either pinch the edges or fold them over to form a crust.\n10. Drizzle additional olive oil (about a Tablespoon) over the top of the pizza and use your pastry brush to brush the entire surface of the pizza (including the crust) with olive oil.\n11. Use a fork to poke holes all over the center of the pizza to keep the dough from bubbling up in the oven.\n"""\nGiven we put the ingredients on the pizza disc in the following order:\n| Order      |\n| <Sauce>    |\n| <Toppings> |\nWhen we cook the pizza\nThen the <Type> pizza is ready to eat\nScenarios:\n| Type        | Sauce  | Toppings                   | Size |\n| Margherita  | tomato | mozzarella,basil           | 28cm |\n| Margherita  | tomato | mozzarella,basil           | 32cm |\n| Pepperoni   | tomato | pepperoni,mozzarella       | 28cm |\n| Pepperoni   | tomato | pepperoni,mozzarella       | 32cm |\n| Hawaiian    | tomato | ham,pineapple,mozzarella   | 28cm |\n| Hawaiian    | tomato | ham,pineapple,mozzarella   | 32cm |\n| Veggie      | pesto  | bell peppers,olive,spinach | 28cm |\n| Veggie      | pesto  | bell peppers,olive,spinach | 32cm |\n| BBQ Chicken | BBQ    | chicken,onion,cilantro     | 28cm |\n| BBQ Chicken | BBQ    | chicken,onion,cilantro     | 32cm |'
        )


def test_save_as_json() -> None:
    """Test."""

    expected_scenario_json = {
        "tags": [],
        "name": "Make hotdog",
        "steps": [
            {"step": "Given", "description": "the sausage is cooked"},
            {"step": "When", "description": "the sausage is put into a bun"},
            {"step": "Then", "description": "the hotdog is ready to eat"},
        ],
        "template_table": None,
    }
    scenario.save_as_json(scenario.load("tests/data/simple_scenario.feature"), "tests/data/saved_scenario.json")
    actual_scenario_json = json.loads(open("tests/data/saved_scenario.json", "r", encoding="utf-8").read())
    assert expected_scenario_json == actual_scenario_json

    expected_scenario_json = {
        "tags": ["american", "canadian", "italian"],
        "name": "Make pizza",
        "steps": [
            {
                "step": "Given",
                "description": "we knead the dough into a <Size> wide pizza disc",
                "docstring-language": "markdown",
                "docstring": "# Pizza Dough Recipe\n\n> Source: [Sam Merritt - The Best Pizza Dough Recipe (article)](https://sugarspunrun.com/the-best-pizza-dough-recipe/)\n\n## Ingredients\n\n- [ ] 2-2 \u2153 cups all-purpose flour OR bread flour divided (250-295g)\n- [ ] 1 packet instant yeast (2 \u00bc teaspoon)\n- [ ] 1 \u00bd teaspoons sugar\n- [ ] \u00be teaspoon salt\n- [ ] \u215b-\u00bc teaspoon garlic powder and/or dried basil leaves optional\n- [ ] 2 Tablespoons olive oil + additional\n- [ ] \u00be cup warm water (175ml)\n\n## Instructions\n\n1. Combine 1 cup (125g) of flour, instant yeast, sugar, and salt in a large bowl. If desired, add garlic powder and dried basil at this point as well.\n2. Add olive oil and warm water and use a wooden spoon to stir well very well.\n3. Gradually add another 1 cup (125g) of flour. Add any additional flour as needed (I've found that sometimes I need as much as an additional \u2153 cup), stirring until the dough is forming into a cohesive, elastic ball and is beginning to pull away from the sides of the bowl (see video above recipe for visual cue). The dough will still be slightly sticky but still should be manageable with your hands.\n4. Drizzle a separate, large, clean bowl generously with olive oil and use a pastry brush to brush up the sides of the bowl.\n5. Lightly dust your hands with flour and form your pizza dough into a round ball and transfer to your olive oil-brushed bowl. Use your hands to roll the pizza dough along the inside of the bowl until it is coated in olive oil, then cover the bowl tightly with plastic wrap and place it in a warm place.\n6. Allow dough to rise for 30 minutes or until doubled in size. If you intend to bake this dough into a pizza, I also recommend preheating your oven to 425F (215C) at this point so that it will have reached temperature once your pizza is ready to bake.\n7. Once the dough has risen, use your hands to gently deflate it and transfer to a lightly floured surface and knead briefly until smooth (about 3-5 times).\n8. Use either your hands or a rolling pin to work the dough into 12\" circle.\n9. Transfer dough to a parchment paper lined pizza pan and either pinch the edges or fold them over to form a crust.\n10. Drizzle additional olive oil (about a Tablespoon) over the top of the pizza and use your pastry brush to brush the entire surface of the pizza (including the crust) with olive oil.\n11. Use a fork to poke holes all over the center of the pizza to keep the dough from bubbling up in the oven.",
            },
            {"step": "Given", "description": "we put the ingredients on the pizza disc in the following order:", "table": {"Order": ["<Sauce>", "<Toppings>"]}},
            {"step": "When", "description": "we cook the pizza"},
            {"step": "Then", "description": "the <Type> pizza is ready to eat"},
        ],
        "template_table": {
            "Type": ["Margherita", "Margherita", "Pepperoni", "Pepperoni", "Hawaiian", "Hawaiian", "Veggie", "Veggie", "BBQ Chicken", "BBQ Chicken"],
            "Sauce": ["tomato", "tomato", "tomato", "tomato", "tomato", "tomato", "pesto", "pesto", "BBQ", "BBQ"],
            "Toppings": [
                "mozzarella,basil",
                "mozzarella,basil",
                "pepperoni,mozzarella",
                "pepperoni,mozzarella",
                "ham,pineapple,mozzarella",
                "ham,pineapple,mozzarella",
                "bell peppers,olive,spinach",
                "bell peppers,olive,spinach",
                "chicken,onion,cilantro",
                "chicken,onion,cilantro",
            ],
            "Size": ["28cm", "32cm", "28cm", "32cm", "28cm", "32cm", "28cm", "32cm", "28cm", "32cm"],
        },
    }
    scenario.save_as_json(scenario.load("tests/data/complex_scenario.feature"), "tests/data/saved_scenario.json")
    actual_scenario_json = json.loads(open("tests/data/saved_scenario.json", "r", encoding="utf-8").read())
    assert expected_scenario_json == actual_scenario_json
