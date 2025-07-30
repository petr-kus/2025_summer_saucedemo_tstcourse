# SauceDemo Test Framework 2.0 - Advanced PyTest + POM

**Author:** Tomas Bartko  
**Date:** 2025-07-30  
**Course:** Test Automation Summer Course - Lesson 8  
**Framework:** PyTest + Advanced Page Object Model + Domain Language

## 🚀 **Overview**

Advanced test automation framework built from the ground up with enterprise-grade practices:

- **🎯 Domain Language**: Business-readable test methods
- **🏗️ Advanced POM**: Enhanced Page Object Model with comprehensive error handling
- **📊 Smart Logging**: Structured logging with test steps, actions, and verifications
- **📸 Auto Screenshots**: Automatic failure screenshots with Allure integration
- **🔧 PyTest Integration**: Modern test framework with fixtures and parametrization
- **📈 Rich Reporting**: HTML reports + Allure integration
- **⚙️ Configuration Management**: Centralized config with environment support

## 🏗️ **Architecture**

### **Framework Structure**
```
lekce_8/
├── config/                 # Configuration management
│   ├── __init__.py
│   └── test_config.py     # Centralized configuration
├── pages/                 # Page Object Model
│   ├── __init__.py
│   ├── base_page.py       # Enhanced base page with domain language
│   └── login_page.py      # Login page with comprehensive methods
├── tests/                 # PyTest test suites
│   ├── __init__.py
│   └── test_login_scenarios.py  # Login test scenarios
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── logging_config.py  # Advanced logging setup
│   └── screenshot_helper.py  # Screenshot management
├── conftest.py           # PyTest fixtures and configuration
├── pytest.ini           # PyTest settings
└── requirements.txt      # Dependencies
```

### **Key Components**

#### **🎯 Domain Language Methods**
```python
# Business-readable test steps
login_page.navigate_to_login_page()
login_page.login_as_standard_user()  
login_page.verify_login_was_successful()

# Comprehensive flows
login_page.perform_complete_valid_login_flow(UserType.STANDARD)
```

#### **📊 Advanced Logging**
```python
logger.test_step("Navigate to login page")
logger.test_action("Click element", element="login_button")
logger.test_verification("Login success", "inventory.html", current_url, passed)
logger.test_data("User credentials", {"user": "standard_user"})
```

#### **🔧 Smart Configuration**
```python
# Environment-aware configuration
config.browser = Browser.CHROME
config.headless = True
config.screenshot_on_failure = True
```

## 🧪 **Test Coverage**

### **Login Scenarios**
- ✅ **Standard User Login** - Happy path authentication
- ✅ **Problem User Login** - Known issue user authentication  
- ✅ **Invalid Credentials** - Rejection with proper error messages
- ✅ **Empty Username/Password** - Field validation
- ✅ **Locked Out User** - Account lockout handling
- ✅ **Form Element Validation** - UI component verification
- ✅ **Integration Flows** - End-to-end login processes

### **Test Markers**
```python
@pytest.mark.smoke         # Critical functionality
@pytest.mark.regression    # Full test coverage
@pytest.mark.user_management  # User-related tests
```

## 🚀 **Installation & Setup**

### **Quick Start**
```bash
# Clone and navigate
git clone <repository>
cd lekce_8

# Run installation script
./install_dependencies.sh

# Activate virtual environment
source venv/bin/activate
```

### **Manual Setup**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🏃 **Running Tests**

### **Basic Test Execution**
```bash
# Run all tests with verbose output
pytest tests/ -v

# Run only smoke tests
pytest tests/ -m smoke -v

# Run specific test file
pytest tests/test_login_scenarios.py -v
```

### **Advanced Reporting**

#### **HTML Reports**
```bash
# Generate HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html

# Open report
open reports/report.html
```

#### **Allure Reports**
```bash
# Generate Allure results
pytest tests/ --alluredir=allure-results

# Serve interactive report
allure serve allure-results
```

### **Test Filtering**
```bash
# Run regression tests only
pytest tests/ -m regression

# Run user management tests
pytest tests/ -m user_management

# Run with custom markers
pytest tests/ -m "smoke or regression"
```

## 📊 **Features Highlights**

### **🎯 Domain Language Excellence**
- **Self-Documenting**: Methods named in business language
- **Expert Readable**: Non-technical stakeholders can understand test flow
- **Maintainable**: Clear separation of concerns

### **🏗️ Advanced Page Object Model**
- **BasePage Foundation**: Common functionality for all pages
- **Smart Waiting**: Intelligent element waiting strategies
- **Error Handling**: Comprehensive exception handling with screenshots
- **Element Safety**: Safe element interactions with logging

### **📊 Comprehensive Logging**
- **Structured Logging**: Test steps, actions, verifications, data
- **Multiple Outputs**: Console + file logging
- **Context Aware**: Method names, line numbers, timestamps
- **Debug Support**: Screenshot logging and failure context

### **🔧 Enterprise Configuration**
- **Environment Variables**: Configurable via env vars
- **User Types**: Enum-based user management
- **Browser Support**: Extensible browser configuration
- **Test Data**: Centralized test data management

### **📸 Smart Screenshots**
- **Failure Capture**: Automatic screenshots on test failures
- **Verification Shots**: Screenshots for important verifications
- **Allure Integration**: Screenshots attached to reports
- **Cleanup**: Automatic old screenshot cleanup

### **🧪 PyTest Integration**
- **Modern Fixtures**: Browser management, user credentials
- **Parametrization**: Data-driven testing support
- **Markers**: Organized test categorization
- **Hooks**: Custom test lifecycle hooks

## 🎯 **Best Practices Implemented**

### **✅ Domain Language**
```python
# ❌ Bad - Technical language
def test_login():
    driver.find_element(By.ID, "user-name").send_keys("standard_user")

# ✅ Good - Domain language  
def test_standard_user_login():
    login_page.login_as_standard_user()
    assert login_page.verify_login_was_successful()
```

### **✅ Comprehensive Logging**
```python
# Every action is logged with context
logger.test_step("Perform login as standard user")
logger.test_action("Enter username", value="standard_user")
logger.test_verification("Login success", expected="inventory.html", actual=url)
```

### **✅ Error Handling**
```python
# Graceful failure handling with screenshots
try:
    element = self.find_clickable_element(locator)
    element.click()
except TimeoutException:
    self.capture_failure_screenshot("element_not_clickable")
    raise
```

### **✅ Configuration Management**
```python
# Centralized, environment-aware configuration
@dataclass
class TestConfig:
    browser: Browser = Browser.CHROME
    headless: bool = True
    base_url: str = "https://www.saucedemo.com/"
```

## 📈 **Test Reports**

Framework generates multiple report formats:

1. **Console Output**: Real-time test progress with structured logging
2. **HTML Reports**: Self-contained test reports with failure details
3. **Allure Reports**: Interactive dashboard with test history
4. **Log Files**: Detailed log files with full test context
5. **Screenshots**: Automatic failure and verification screenshots

## 🔄 **Extensibility**

Framework designed for easy extension:

- **New Page Objects**: Extend BasePage for new pages
- **Additional Tests**: Use existing fixtures and utilities
- **Custom Markers**: Add new test categories
- **Browser Support**: Add new browser configurations
- **Reporting**: Integrate additional reporting tools

## 🎯 **Learning Outcomes**

This framework demonstrates:

1. **Professional Test Structure** - Enterprise-grade organization
2. **Domain Language** - Business-readable test automation
3. **Modern PyTest** - Fixtures, markers, and configurations
4. **Advanced POM** - Scalable page object architecture
5. **Error Handling** - Robust failure management
6. **Logging Best Practices** - Comprehensive test observability
7. **Configuration Management** - Environment-aware testing
8. **Rich Reporting** - Multiple reporting strategies

---

**Framework Version**: 2.0  
**PyTest Compatible**: ✅  
**Allure Compatible**: ✅  
**CI/CD Ready**: ✅  
**Production Ready**: ✅