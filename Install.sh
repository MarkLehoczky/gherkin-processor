#!/bin/bash

PACKAGE_NAME="gherkin-processor"

# Check if pip is installed; otherwise exit with an error message
if ! command -v pip &> /dev/null; then
    echo "ERROR: pip is not installed!"
    echo "Please install pip before running this script."
    echo
    echo "Exiting..."
    sleep 5
    exit 1
fi

# Check if the package is already installed
pip show "$PACKAGE_NAME" &> /dev/null

# If the package is installed, upgrade it; otherwise install it
if [ $? -eq 0 ]; then
    echo "Package '$PACKAGE_NAME' is already installed. Upgrading package..."
    echo
    pip install --quiet --upgrade --compile .

    # Check if pip upgrade was successful
    if [ $? -eq 0 ]; then
        echo
        echo "Upgrade completed successfully!"
    else
        echo
        echo "ERROR: Upgrade failed!"
        echo
        echo "Exiting..."
        sleep 5
        exit 2
    fi
else
    echo "Installing package..."
    echo
    pip install --compile .

    # Check if pip installation was successful
    if [ $? -eq 0 ]; then
        echo
        echo "Installation completed successfully!"
        echo
        echo "Exiting..."
        sleep 5
        exit 0
    else
        echo
        echo "ERROR: Installation failed!"
        echo
        echo "Exiting..."
        sleep 5
        exit 2
    fi
fi
