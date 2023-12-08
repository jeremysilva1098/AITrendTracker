#!/bin/bash

# Check if the PYTHON_ENV_PATH variable is set
if [ -n "$PYTHON_ENV_PATH" ]; then
    # Use the provided Python environment path
    PYTHON_EXECUTABLE="$PYTHON_ENV_PATH/bin/python3"
else
    # Use the default Python executable
    PYTHON_EXECUTABLE="python3"
fi

# Rest of your script goes here
$PYTHON_EXECUTABLE research/main.py
$PYTHON_EXECUTABLE news-and-blogs/main.py
