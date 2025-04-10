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
- **Arguments:** `-h`, `--help`
- **Examples**:
  ```sh
  gherkin-processor -h
  gherkin-processor --help
  ```

### Input path

- **Description**: Specify the input file path.
- **Type**: String (required)
- **Arguments:** `-i`, `--input`
- **Examples**:
  ```sh
  gherkin-processor -i gherkin/example.feature
  gherkin-processor --input gherkin/example.feature
  gherkin-processor -i "gherkin/example.feature"
  gherkin-processor --input "gherkin/example.feature"
  gherkin-processor -i=gherkin/example.feature
  gherkin-processor --input=gherkin/example.feature
  gherkin-processor -i="gherkin/example.feature"
  gherkin-processor --input="gherkin/example.feature"
  ```

### Output path

- **Description**: Specify the output file path for saving the processed file.
- **Type**: String (optional)
- **Arguments:** `-o`, `--output`
- **Examples**:
  ```sh
  gherkin-processor --input gherkin/example.feature -o gherkin/output/example.feature
  gherkin-processor --input gherkin/example.feature --output gherkin/output/example.feature
  gherkin-processor --input gherkin/example.feature -o "gherkin/output/example.feature"
  gherkin-processor --input gherkin/example.feature --output "gherkin/output/example.feature"
  gherkin-processor --input gherkin/example.feature -o=gherkin/output/example.feature
  gherkin-processor --input gherkin/example.feature --output=gherkin/output/example.feature
  gherkin-processor --input gherkin/example.feature -o="gherkin/output/example.feature"
  gherkin-processor --input gherkin/example.feature --output="gherkin/output/example.feature"
  ```

### Print Gherkin syntax

- **Description**: Write the input file's Gherkin syntax to standard output.
- **Type**: Flag (optional)
- **Arguments:** `-p`, `--print`
- **Examples**:
  ```sh
  gherkin-processor --input features/example.feature -p
  gherkin-processor --input features/example.feature --print
  ```

### Save as Gherkin

- **Description**: Save the file in Gherkin format.
- **Type**: Flag (optional)
- **Arguments:** `-s`, `--save`, `--save-gherkin`
- **Examples**:
  ```sh
  gherkin-processor --input features/example.feature -s
  gherkin-processor --input features/example.feature --save
  gherkin-processor --input features/example.feature --save-gherkin
  ```

### Save as JSON

- **Description**: Save the file in JSON format.
- **Type**: Flag (optional)
- **Arguments:** `-j`, `--json`, `--save-json`
- **Examples**:
  ```sh
  gherkin-processor --input features/example.feature -j
  gherkin-processor --input features/example.feature --json
  gherkin-processor --input features/example.feature --save-json
  ```

### Force confirmation

- **Description**: Automatically confirm all user input prompts with 'yes'.
- **Type**: Flag (optional)
- **Arguments:** `-y`, `--yes`, `--force-yes`
- **Examples**:
  ```sh
  gherkin-processor --input features/example.feature -y
  gherkin-processor --input features/example.feature --yes
  gherkin-processor --input features/example.feature --force-yes
  ```

### Validate syntax

- **Description**: Validate the syntax of the input file.
- **Type**: Flag (optional)
- **Arguments:** `-v`, `--validate`
- **Examples**:
  ```sh
  gherkin-processor --input features/example.feature -v
  gherkin-processor --input features/example.feature --validate
  ```
