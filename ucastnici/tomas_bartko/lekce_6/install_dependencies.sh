#!/bin/bash

# Install dependencies for SauceDemo tests
# Author: Tomas Bartko
# Date: 2025-07-30

echo "Setting up SauceDemo test environment..."

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

echo "Setup completed successfully!"
echo ""
echo "To run the tests:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run tests: python test.py"
echo ""
echo "Make sure you have Chrome browser installed!"