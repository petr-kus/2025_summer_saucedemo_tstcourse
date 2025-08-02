#!/bin/bash

echo "🚀 Setting up SauceDemo Test Framework 2.0 with PyTest..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "✅ Installation complete!"
echo ""
echo "To activate virtual environment:"
echo "source venv/bin/activate"
echo ""
echo "To run tests:"
echo "pytest tests/ -v"
echo ""
echo "To run tests with HTML report:"
echo "pytest tests/ -v --html=reports/report.html --self-contained-html"
echo ""
echo "To run tests with Allure report:"
echo "pytest tests/ --alluredir=allure-results"
echo "allure serve allure-results"