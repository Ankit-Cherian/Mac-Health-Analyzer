#!/bin/bash
# Launch script for Mac Health Pulse

# Change to project root directory (parent of scripts/)
cd "$(dirname "$0")/.."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

# Check if required packages are installed
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "Installing required dependencies..."
    pip3 install -r requirements.txt
fi

# Run the application
echo "Starting Mac Health Pulse..."
PYTHONPATH=src python3 -m main

