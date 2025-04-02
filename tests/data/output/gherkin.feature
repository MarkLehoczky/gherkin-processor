Feature: Making breakfast
Describes a morning routine regarding breakfast making of an average person.
Rule: Only one breakfast meal should be prepared
  The morning routine should include breakfast for only one person.
    The default assumption is that every breakfast comes with coffee.
Given I have coffee grounds
Given I add hot water
Given I get a cup of coffee
@american
@canadian
@european
Scenario: Making pancake
Given I have pancake mix prepared the following way:
"""
            Add ½ cup milk, 1 cup baking mix, 1 tbsp olive oil and 1 egg into a bowl.
            Stir the mix until the texture is consistent.
"""
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
Given I prepare the eggs by <preparing>
When I <cook> the eggs for "<minute>" minutes
Then I get "<name>" eggs
| name          | preparing                        | cook  | minute |
| Sunny side up | cracking it into a pan           | fry   | 3      |
| Scrambled     | mixing it till consistency       | fry   | 5      |
| Soft boiled   | placing it in boiling water      | boil  | 6      |
| Hard boiled   | placing it in boiling water      | boil  | 12     |
| Poached       | cracking it into simmering water | poach | 4      |