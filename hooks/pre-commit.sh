#!/bin/bash

overall_status=0

echo ""
echo "=================================================="
echo "           GIT PRE-COMMIT HOOK STARTED            "
echo "--------------------------------------------------"

run_check() {
  local name=$1
  shift
  "$@" >> /dev/null 2>&1
  exit_status=$?
  if [ $exit_status -ne 0 ]; then
    echo "${name} failed with exit code ${exit_status}"
    overall_status=1
  else
    echo "${name} passed"
  fi
}

run_check "Complete Test Suite" pytest --cov --cov-fail-under=90 tests/
echo "------------------------------"

run_check "Project Security Scan" bandit --recursive gherkin_processor/
echo "------------------------------"

run_check "Linting Analysis" pylint --max-line-length=160 --fail-under=9.90 gherkin_processor/
run_check "Type Hint Analysis" mypy --strict gherkin_processor/
run_check "Code Metrics Analysis (cyclomatic complexity)" radon cc gherkin_processor/
run_check "Code Metrics Analysis (maintainability index)" radon mi gherkin_processor/
echo "------------------------------"

run_check "Code Style Check" pycodestyle --max-line-length=160 gherkin_processor/
run_check "Documentation Style Check" pydocstyle gherkin_processor/

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
