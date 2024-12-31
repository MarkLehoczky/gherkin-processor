Scenario: Make pizza
Given we knead the dough into a <Size> wide pizza disc
And we put the ingredients on the pizza disc in the following order:
| Order      |
| <Sauce>    | Olive oil |
| <Toppings> |
When we cook the pizza
Then the <Type> pizza is ready to eat