# Utilities Documentation

## Overview

This document provides detailed information about utility functions for processing, loading, saving, and validating Gherkin text.

---

### `process`

- **Description**: Processes Gherkin text and returns a `Gherkin` object.
- **Arguments**:
  - `gherkin_text` (`str`): The Gherkin text to process.
  - `validate_text` (`bool`, optional): Enables syntax validation during processing. Defaults to `False`.
- **Returns**: `Gherkin` - The processed Gherkin object.
- **Raises**:
  - `TypeError`: If `gherkin_text` is not a string.
  - `ValueError`: If validation fails due to syntax issues.
- **Usage**:
  ```python
  from gherkin_processor.utils import process

  # Process Gherkin text
  gherkin_obj = process("Feature: Example feature")

  # Process with validation
  try:
      gherkin_obj = process("Feature: Example feature", validate_text=True)
  except Exception as e:
      print(e)
  ```

---

### `load`

- **Description**: Loads a Gherkin file and returns a `Gherkin` object.
- **Arguments**:
  - `file_path` (`str`): Path to the Gherkin file.
  - `validate_text` (`bool`, optional): Enables syntax validation during loading. Defaults to `False`.
- **Returns**: `Gherkin | None` - The loaded Gherkin object, or `None` if the file does not exist.
- **Raises**:
  - `ValueError`: If validation fails due to syntax issues.
- **Usage**:
  ```python
  from gherkin_processor.utils import load

  # Load Gherkin file
  gherkin_obj = load("gherkin/example.feature")

  # Load with validation
  try:
      gherkin_obj = load("gherkin/example.feature", validate_text=True)
  except Exception as e:
      print(e)
  ```

---

### `save`

- **Description**: Saves a `Gherkin` object to a file in the specified format.
- **Arguments**:
  - `gherkin` (`Gherkin`): The Gherkin object to save.
  - `file_path` (`str`): Path to the output file.
  - `mode` (`str`, optional): Format to save the file in (`"GHERKIN"` or `"JSON"`). Defaults to `"GHERKIN"`.
  - `override_existing_file` (`bool`, optional): Whether to overwrite an existing file. Defaults to `False`.
- **Returns**: `bool` - `True` if the file was saved successfully, otherwise `False`.
- **Usage**:
  ```python
  from gherkin_processor.utils import save

  # Save Gherkin object
  success = save(gherkin_obj, "gherkin/output/example.feature")

  # Save with JSON format and overwrite
  success = save(gherkin_obj, "gherkin/output/example.json", mode="JSON", override_existing_file=True)
  ```

---

### `validate`

- **Description**: Validates the syntax of Gherkin text.
- **Arguments**:
  - `gherkin_text` (`str`): The Gherkin text to validate.
- **Raises**:
  - `TypeError`: If `gherkin_text` is not a string.
  - `ValueError`: If validation fails due to syntax issues.
- **Usage**:
  ```python
  from gherkin_processor.utils import validate

  # Validate Gherkin text
  validate("Feature: Example feature")

  # Validate with error handling
  try:
      validate("Feature: Example feature")
  except Exception as e:
      print(e)
  ```

---

### `is_valid`

- **Description**: Checks if the Gherkin text is valid.
- **Arguments**:
  - `gherkin_text` (`str`): The Gherkin text to validate.
- **Returns**: `bool` - `True` if the syntax is valid, otherwise `False`.
- **Usage**:
  ```python
  from gherkin_processor.utils import is_valid

  # Check if Gherkin text is valid
  is_valid_text = is_valid("Feature: Example feature")
  ```

---

### `issue`

- **Description**: Returns validation issues for Gherkin text, if any.
- **Arguments**:
  - `gherkin_text` (`str`): The Gherkin text to validate.
- **Returns**: `str` - An error message if validation fails, otherwise an empty string.
- **Usage**:
  ```python
  from gherkin_processor.utils import issue

  # Check for issues in Gherkin text
  validation_issue = issue("Feature: Example feature")
  if validation_issue:
      print(f"Issue found: {validation_issue}")
  ```
