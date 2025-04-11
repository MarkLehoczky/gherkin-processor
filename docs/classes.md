# Gherkin Processor Classes

This document provides an overview of the classes used in the Gherkin Processor project.

## Gherkin

Represents a Gherkin file and its components.

### Attributes
- `file (Optional[str])`: The file path of the Gherkin file being processed.
- `feature (Feature)`: The [feature](#feature) component of the Gherkin file.
- `rule (Rule)`: The [rule](#rule) component of the Gherkin file.
- `background (Background)`: The [background](#background) component of the Gherkin file.
- `scenarios (List[Scenario])`: A list of [scenarios](#scenario) defined in the Gherkin file.

### Methods
- `to_string() -> str`: Converts the Gherkin object to a string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the Gherkin object to a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes and validates the Gherkin text.

---

## Feature

Represents a Gherkin feature.

### Attributes
- `name (str)`: The name of the feature.
- `description (str | None)`: The description of the feature.

### Methods
- `to_string() -> str`: Converts the feature to a string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the feature to a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes and validates the feature text.

---

## Rule

Represents a Gherkin rule.

### Attributes
- `name (str | None)`: The name of the rule.
- `description (str | None)`: The description of the rule.

### Methods
- `to_string() -> str`: Converts the rule to a string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the rule to a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes and validates the rule text.

---

## Background

Represents a Gherkin background.

### Attributes
- `description (str | None)`: The description of the background.
- `steps (List[Step] | None)`: The [steps](#step) in the background.

### Methods
- `to_string() -> str`: Converts the background to a string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the background to a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes and validates the background text.

---

## Scenario

Represents a Gherkin scenario.

### Attributes
- `tags (List[str] | None)`: The tags associated with the scenario.
- `name (str)`: The name of the scenario.
- `description (str | None)`: The description of the scenario.
- `steps (List[Step])`: The [steps](#step) in the scenario.
- `outline (Dict[str, List[str]] | None)`: The outline table for scenario outlines.

### Methods
- `to_string() -> str`: Converts the scenario to a string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the scenario to a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes and validates the scenario text.

---

## Step

Represents a single step in a Gherkin scenario.

### Attributes
- `type (str)`: The type of the step (e.g., Given, When, Then, But).
- `text (str)`: The text of the step.
- `table (Dict[str, List[str]] | None)`: The table associated with the step, if any.
- `doc_string (str | None)`: The doc-string associated with the step, if any.

### Methods
- `to_string() -> str`: Converts the step to a string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the step to a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes and validates the step text.
