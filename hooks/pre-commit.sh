#!/bin/bash
# pre-commit git hook script

# Initialize overall status to success.
overall_status=0

echo ""
echo "=================================================="
echo "           GIT PRE-COMMIT HOOK STARTED            "
echo "--------------------------------------------------"
# Function to run a command and record failure if it occurs.
run_check() {
  local name=$1
  shift
  echo "Running ${name}..."
  "$@" >> /dev/null 2>&1
  exit_status=$?
  if [ $exit_status -ne 0 ]; then
    echo "${name} failed with exit code ${exit_status}"
    overall_status=1
  else
    echo "${name} passed."
  fi
}

# Code functionality check
run_check "pytest" pytest --cov --cov-fail-under=90 tests/
echo "------------------------------"

# Code security check
run_check "bandit" bandit --recursive gherkin_processor/
echo "------------------------------"

# Code Linting check
run_check "pylint" pylint --max-line-length=160 --fail-under=9.90 gherkin_processor/
echo "------------------------------"
run_check "mypy" mypy --strict gherkin_processor/
echo "------------------------------"

# Code Metrics check
run_check "radon cc" radon cc gherkin_processor/
echo "------------------------------"
run_check "radon mi" radon mi gherkin_processor/
echo "------------------------------"

# Code Format check
run_check "pycodestyle" pycodestyle --max-line-length=160 gherkin_processor/
echo "------------------------------"
run_check "pydocstyle" pydocstyle gherkin_processor/

# Final check for overall status
if [ $overall_status -ne 0 ]; then
  echo "--------------------------------------------------"
  echo "       ONE OR MORE PRE-COMMIT HOOKS FAILED        "
  echo "=================================================="
  echo.
  exit $overall_status
fi

echo "--------------------------------------------------"
echo "     ALL PRE-COMMIT HOOK PASSED SUCCESSFULLY      "
echo "=================================================="
echo ""
exit 0
