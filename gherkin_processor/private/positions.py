"""Define allowed positions for Gherkin components.

This module provides dictionaries that define the valid positions for various Gherkin components
such as features, rules, backgrounds, scenarios, and steps. These dictionaries are used to validate
the structure and syntax of Gherkin files during processing.
"""

from typing import Dict, List

given_step_collection = ["GIVEN", "GIVEN TABLE", "GIVEN DOC-STRING"]
when_step_collection = ["WHEN", "WHEN TABLE", "WHEN DOC-STRING"]
then_step_collection = ["THEN", "THEN TABLE", "THEN DOC-STRING"]
but_step_collection = ["BUT", "BUT TABLE", "BUT DOC-STRING"]

ALLOWED_POSITIONS: Dict[str, List[str]] = {
    "FEATURE": ["<BEGINNING>"],
    "RULE": ["FEATURE"],
    "BACKGROUND": ["FEATURE", "RULE"],

    "TAG": ["FEATURE", "RULE", "BACKGROUND", "TAG"] + given_step_collection + then_step_collection + but_step_collection,
    "SCENARIO": ["FEATURE", "RULE", "BACKGROUND", "TAG", "SCENARIO", "OUTLINE TABLE"] + given_step_collection + then_step_collection + but_step_collection,

    "GIVEN": ["BACKGROUND", "SCENARIO"] + given_step_collection,
    "GIVEN TABLE": ["GIVEN", "GIVEN TABLE"],
    "GIVEN DOC-STRING": ["GIVEN", "GIVEN DOC-STRING"],

    "WHEN": given_step_collection + when_step_collection + then_step_collection + but_step_collection,
    "WHEN TABLE": ["WHEN", "WHEN TABLE"],
    "WHEN DOC-STRING": ["WHEN", "WHEN DOC-STRING"],

    "THEN": when_step_collection + then_step_collection,
    "THEN TABLE": ["THEN", "THEN TABLE"],
    "THEN DOC-STRING": ["THEN", "THEN DOC-STRING"],

    "BUT": then_step_collection + but_step_collection,
    "BUT TABLE": ["BUT", "BUT TABLE"],
    "BUT DOC-STRING": ["BUT", "BUT DOC-STRING"],

    "OUTLINE": then_step_collection + but_step_collection,
    "OUTLINE TABLE": ["OUTLINE", "OUTLINE TABLE"]
}

ALLOWED_BACKGROUND_POSITIONS: Dict[str, List[str]] = {
    "BACKGROUND": ["<BEGINNING>"],
    "BACKGROUND DESCRIPTION": ["BACKGROUND", "BACKGROUND DESCRIPTION"],

    "GIVEN": ["BACKGROUND", "BACKGROUND DESCRIPTION"] + given_step_collection,
    "GIVEN TABLE": ["GIVEN", "GIVEN TABLE"],
    "GIVEN DOC-STRING": ["GIVEN", "GIVEN DOC-STRING"],

    "WHEN": [],
    "THEN": [],
    "BUT": [],
}

ALLOWED_SCENARIO_POSITIONS: Dict[str, List[str]] = {
    "TAG": ["<BEGINNING>", "TAG"],
    "SCENARIO": ["<BEGINNING>", "TAG"],
    "SCENARIO DESCRIPTION": ["SCENARIO", "SCENARIO DESCRIPTION"],

    "GIVEN": ["SCENARIO", "SCENARIO DESCRIPTION"] + given_step_collection,
    "GIVEN TABLE": ["GIVEN", "GIVEN TABLE"],
    "GIVEN DOC-STRING": ["GIVEN", "GIVEN DOC-STRING"],

    "WHEN": given_step_collection + when_step_collection + then_step_collection + but_step_collection,
    "WHEN TABLE": ["WHEN", "WHEN TABLE"],
    "WHEN DOC-STRING": ["WHEN", "WHEN DOC-STRING"],

    "THEN": when_step_collection + then_step_collection,
    "THEN TABLE": ["THEN", "THEN TABLE"],
    "THEN DOC-STRING": ["THEN", "THEN DOC-STRING"],

    "BUT": then_step_collection + but_step_collection,
    "BUT TABLE": ["BUT", "BUT TABLE"],
    "BUT DOC-STRING": ["BUT", "BUT DOC-STRING"],

    "OUTLINE": then_step_collection + but_step_collection,
    "OUTLINE TABLE": ["OUTLINE", "OUTLINE TABLE"]
}
