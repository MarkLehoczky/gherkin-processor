# Module Documentation

## Overview

Modules provide high-level Gherkin utilities for processing, loading, saving, and validating Gherkin text.

---

### Process

- **Description**: Process Gherkin text and return a Gherkin object.
- **Type**: Function
- **Arguments**:
  - `gherkin_text` (str): The Gherkin text to process.
  - `validate_text` (bool, optional): Whether to validate the text. Defaults to `False`.
- **Returns**: `Gherkin` - The processed Gherkin object.
- **Raises**:
  - `TypeError`: If `gherkin_text` is not a string.
  - `ValueError`: If `validate_text` is `True` and the Gherkin syntax has issues.
- **Examples**:
  ```python
  from gherkin_processor import Gherkin
  from gherkin_processor.utils import process

  # Without optional parameters
  gherkin_obj: Gherkin = process("Feature: Example feature")

  # With optional parameters and error catch
  try:
    gherkin_obj: Gherkin = process("gherkin/example.feature", validate_text=True)
  except Exception as e:
    print(e)
  ```

### Load

- **Description**: Load a Gherkin file and return a Gherkin object.
- **Type**: Function
- **Arguments**:
  - `file_path` (str): The path to the Gherkin file.
  - `validate_text` (bool, optional): Whether to validate the file content. Defaults to `False`.
- **Returns**: `Gherkin | None` - The Gherkin object if the file exists and is valid, otherwise `None`.
- **Raises**:
  - `TypeError`: If `file_path` is not a string.
  - `ValueError`: If `validate_text` is `True` and the Gherkin syntax has issues.
- **Examples**:
  ```python
  from gherkin_processor import Gherkin
  from gherkin_processor.utils import load

  # Without optional parameters
  gherkin_obj: Gherkin | None = load("gherkin/example.feature")

  # With optional parameters and error catch
  try:
    gherkin_obj: Gherkin | None = load("gherkin/example.feature", validate_text=True)
  except Exception as e:
    print(e)
  ```

### Save

- **Description**: Save a Gherkin object to a file in the specified format.
- **Type**: Function
- **Arguments**:
  - `gherkin` (Gherkin): The Gherkin object to save.
  - `file_path` (str): The path to save the file.
  - `mode` (str, optional): The format to save the file in (`"GHERKIN"`, or `"JSON"`). Defaults to `"GHERKIN"`.
  - `override_existing_file` (bool, optional): Whether to override an existing file. Defaults to `False`.
- **Returns**: `bool` - `True` if the file was saved successfully, otherwise `False`.
- **Raises**:
  - `TypeError`: If `file_path` is not a string.
  - `ValueError`: If `mode` is not one of `"GHERKIN"`, or `"JSON"`.
- **Examples**:
  ```python
  from gherkin_processor import Gherkin
  from gherkin_processor.utils import save

  # Without optional parameters
  success: bool = save(gherkin_obj, "gherkin/output/example.feature")

  # With optional parameters
  success: bool = save(gherkin_obj, "gherkin/output/example.feature", mode="JSON", override_existing_file=True)
  ```

### Validate

- **Description**: Validate Gherkin text by processing it with validation enabled.
- **Type**: Function
- **Arguments**:
  - `gherkin_text` (str): The Gherkin text to validate.
- **Raises**:
  - `TypeError`: If `gherkin_text` is not a string.
  - `ValueError`: If the Gherkin syntax has issues.
- **Examples**:
  ```python
  from gherkin_processor.utils import validate

  # Validate Gherkin text
  validate("Feature: Example feature")

  # Validate Gherkin text with error catch
  try:
    validate("Feature: Example feature")
  except Exception as e:
    print(e)
  ```

### Is valid

- **Description**: Check if the Gherkin text is valid.
- **Type**: Function
- **Arguments**:
  - `gherkin_text` (str): The Gherkin text to validate.
- **Returns**: `bool` - `True` if the text is valid, otherwise `False`.
- **Raises**:
  - `TypeError`: If `gherkin_text` is not a string.
  - `ValueError`: If the Gherkin syntax has issues.
- **Examples**:
  ```python
  from gherkin_processor.utils import is_valid

  # Check if Gherkin text is valid
  is_valid_text: bool = is_valid("Feature: Example feature")
  ```

### Issue

- **Description**: Process Gherkin text and return any validation issues found.
- **Type**: Function
- **Arguments**:
  - `gherkin_text` (str): The Gherkin text to check for issues.
- **Returns**: `str` - An error message if validation fails, otherwise an empty string.
- **Raises**:
  - `TypeError`: If `gherkin_text` is not a string.
  - `ValueError`: If the Gherkin syntax has issues.
- **Examples**:
  ```python
  from gherkin_processor.utils import issue

  # Check for issues in Gherkin text
  issue: str = issue("Feature: Example feature")
  if issue:
      print(f"Issue found: {issue}")
  ```
