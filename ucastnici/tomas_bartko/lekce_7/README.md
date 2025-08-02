# SauceDemo Automated Tests

**Author:** Tomas Bartko  
**Date:** 2025-07-30  
**Course:** Test Automation Summer Course

## Description

Extended automated test suite for SauceDemo website (https://www.saucedemo.com/) using Selenium WebDriver.

### Test Coverage

The test suite includes three main test scenarios:

1. **Standard User Shopping Flow**
   - Login with valid credentials (standard_user)
   - Add multiple products to cart
   - Verify cart badge and cart page functionality
   - Check checkout button availability

2. **Problem User Issues Testing**
   - Login as problem_user (known to have bugs)
   - Attempt to add products to cart
   - Demonstrate and report known product addition issues

3. **Invalid Login Testing**
   - Test login with invalid credentials
   - Verify proper error message display
   - Ensure user stays on login page

### Features

- **Assert-based verification** for all critical steps
- **Multiple user types** testing (standard_user, problem_user, invalid_user)
- **Cart functionality** testing with badge verification
- **Error handling** and negative test cases
- **Configurable Chrome options** (headless mode available)
- **Detailed console output** for test progress tracking

## Installation

1. Run the installation script:
```bash
./install_dependencies.sh
```

2. Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- Chrome browser
- ChromeDriver (automatically managed by webdriver-manager)

## Usage

1. Activate virtual environment:
```bash
source venv/bin/activate
```

2. Run the tests:
```bash
python test.py
```

## Test Results

Expected output:
- Standard user: All functionality should work correctly
- Problem user: May demonstrate known bugs (products not adding to cart)
- Invalid login: Should show proper error message

## Notes

This test suite extends the basic login test from the course with additional functionality including shopping cart interactions, multiple user scenarios, and comprehensive verification steps.