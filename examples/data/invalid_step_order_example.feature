Scenario: Make pizza
Given we knead the dough into a <Size> wide pizza disc
And we put the ingredients on the pizza disc in the following order:
| Order      |
| <Sauce>    |
| <Toppings> |
Then the <Type> pizza is ready to eat
When we cook the pizza