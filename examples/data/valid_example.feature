@food
Scenario: Make hotdog
Given the sausage is cooked
When the sausage is put into a bun
And the following toppings are added:
| Topping |
| ketchup |
| mustard |
| relish  |
Then the hotdog is ready to eat
