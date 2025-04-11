# Command Line Interface Documentation

## Usage

```sh
gherkin-processor [-h] --input INPUT [-o OUTPUT] [-p] [-s] [-j] [-y] [-v]
```

Process and save Gherkin files in different formats.

---

### Help message

- **Description**: Show the help message and exit.
- **Type**: Flag
- **Arguments**: `-h`, `--help`
- **Usage**:
  ```sh
  gherkin-processor -h
  gherkin-processor --help
  ```

### Input path

- **Description**: Specify the input file path.
- **Type**: String (required)
- **Arguments**: `-i`, `--input`
- **Usage**:
  ```sh
  gherkin-processor -i example.feature
  gherkin-processor --input example.feature
  gherkin-processor -i "example.feature"
  gherkin-processor --input "example.feature"
  gherkin-processor -i=example.feature
  gherkin-processor --input=example.feature
  gherkin-processor -i="example.feature"
  gherkin-processor --input="example.feature"
  ```

### Output path

- **Description**: Specify the output file path for saving the processed file.
- **Type**: String (optional)
- **Arguments**: `-o`, `--output`
- **Variables**:
    - `<DIR>`, `<DIRECTORY>`: Replaces the variable with the input file absolute directory path (may cause issues when using relative path)
    - `<NAME>`, `<FILENAME>`: Replaces the variable with the input file name (without extension)
    - `<EXT>`, `<EXTENSION>`: Replaces the variable with the appropriate extension (input file extension for Gherkin format, "json" for Json format) [dot (".") is excluded from it]
- **Usage**:
  ```sh
  gherkin-processor --input example.feature -o output/example.feature
  gherkin-processor --input example.feature --output output/processed.feature
  gherkin-processor --input example.feature -o "output/<NAME>.<EXT>"
  gherkin-processor --input example.feature --output "<DIR>/<NAME>_processed.<EXT>"
  gherkin-processor --input example.feature -o=output/example.feature
  gherkin-processor --input example.feature --output=output/processed.feature
  gherkin-processor --input example.feature -o="output/<NAME>.<EXT>"
  gherkin-processor --input example.feature --output="<DIR>/<NAME>_processed.<EXT>"
  ```

### Print Gherkin syntax

- **Description**: Write the input file's Gherkin syntax to standard output.
- **Type**: Flag (optional)
- **Arguments**: `-p`, `--print`
- **Usage**:
  ```sh
  gherkin-processor --input example.feature -p
  gherkin-processor --input example.feature --print
  ```

### Save as Gherkin

- **Description**: Save the file in Gherkin format.
- **Type**: Flag (optional)
- **Arguments**: `-s`, `--save`, `--save-gherkin`
- **Usage**:
  ```sh
  gherkin-processor --input example.feature -s
  gherkin-processor --input example.feature --save
  gherkin-processor --input example.feature --save-gherkin
  ```

### Save as JSON

- **Description**: Save the file in JSON format.
- **Type**: Flag (optional)
- **Arguments**: `-j`, `--json`, `--save-json`
- **Usage**:
  ```sh
  gherkin-processor --input example.feature -j
  gherkin-processor --input example.feature --json
  gherkin-processor --input example.feature --save-json
  ```

### Force confirmation

- **Description**: Automatically confirm all user input prompts with 'yes'.
- **Type**: Flag (optional)
- **Arguments**: `-y`, `--yes`, `--force-yes`
- **Usage**:
  ```sh
  gherkin-processor --input example.feature -y
  gherkin-processor --input example.feature --yes
  gherkin-processor --input example.feature --force-yes
  ```

### Validate syntax

- **Description**: Validate the syntax of the input file.
- **Type**: Flag (optional)
- **Arguments**: `-v`, `--validate`
- **Usage**:
  ```sh
  gherkin-processor --input example.feature -v
  gherkin-processor --input example.feature --validate
  ```
