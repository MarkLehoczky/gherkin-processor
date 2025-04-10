# Gherkin Processor Classes

This document provides an overview of the classes used in the Gherkin Processor package.

---

## Gherkin

Represents a Gherkin document with its components.

### Attributes

- `file` (Optional[str]): The file path of the Gherkin source (if any).
- `feature` (Feature): The feature definition in the Gherkin document.
- `rule` (Rule): The rule section of the Gherkin document.
- `background` (Background): The background section of the Gherkin document.
- `scenarios` (List[Scenario]): The list of scenarios present in the document.

### Methods

- `to_string() -> str`: Converts the Gherkin document into a formatted string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the Gherkin document into a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes Gherkin syntax content and updates the object accordingly.

---

## Feature

Represents a Gherkin feature with its components.

### Attributes

- `name` (str): The name of the Gherkin feature.
- `description` (Optional[str]): The description of the Gherkin feature (if any).

### Methods

- `to_string() -> str`: Converts the Gherkin feature into a formatted string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the Gherkin feature into a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes Gherkin feature content and updates the object accordingly.

## Rule

Represents a Gherkin rule with its components.

### Attributes

- `name` (Optional[str]): The name of the Gherkin rule (if any).
- `description` (Optional[str]): The description of the Gherkin rule (if any).

### Methods

- `to_string() -> str`: Converts the Gherkin rule into a formatted string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the Gherkin rule into a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes Gherkin rule content and updates the object accordingly.

## Background

Represents a Gherkin background with its components.

### Attributes

- `description` (Optional[str]): The description of the Gherkin background (if any).
- `steps` (Optional[List[Step]]): The list of steps present in the Gherkin background (if any).

### Methods

- `to_string() -> str`: Converts the Gherkin background into a formatted string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the Gherkin background into a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes Gherkin background content and updates the object accordingly.

## Scenario

Represents a Gherkin scenario with its components.

### Attributes

- `tags` (Optional[List[str]]): The tags of the Gherkin scenario (if any).
- `name` (str): The name of the Gherkin scenario.
- `description` (Optional[str]): The description of the Gherkin scenario (if any).
- `steps` (List[Step]): The list of steps present in the Gherkin scenario (if any).
- `outline` (Optional[Dict[str, List[str]]]): The outline table present in the Gherkin scenario (if any).

### Methods

- `to_string() -> str`: Converts the Gherkin scenario into a formatted string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the Gherkin scenario into a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes Gherkin scenario content and updates the object accordingly.

## Step

Represents a Gherkin step with its components.

### Attributes

- `type` (str): The type of the Gherkin step.
- `text` (str): The text of the Gherkin step.
- `table` (Optional[Dict[str, List[str]]]): The table present in the Gherkin step (if any).
- `doc_string` (Optional[str]): The document string present in the Gherkin step (if any).

### Methods

- `to_string() -> str`: Converts the Gherkin step into a formatted string representation.
- `to_dictionary() -> Dict[str, Any]`: Converts the Gherkin step into a dictionary representation.
- `process(text: str, validate: bool) -> bool`: Processes Gherkin step content and updates the object accordingly.
