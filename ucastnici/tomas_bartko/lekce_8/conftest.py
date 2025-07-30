"""
PyTest Configuration and Fixtures
Global test configuration and shared fixtures for SauceDemo test suite
"""

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Removed webdriver-manager imports - using system ChromeDriver
from pathlib import Path

from config import get_config, UserType, Browser
from utils import get_logger, capture_screenshot


@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration for the session"""
    return get_config()


@pytest.fixture(scope="session")
def logger():
    """Provide logger for the session"""
    return get_logger("TestSession")


@pytest.fixture(scope="function")
def browser_driver(request, test_config):
    """
    Create and manage WebDriver instance for each test
    Automatically captures screenshot on test failure
    """
    logger = get_logger("WebDriverFixture")
    
    # Setup driver based on configuration
    if test_config.browser == Browser.CHROME:
        driver = _create_chrome_driver(test_config)
    else:
        raise ValueError(f"Unsupported browser: {test_config.browser}")
    
    # Configure driver
    driver.implicitly_wait(test_config.implicit_wait)
    driver.set_page_load_timeout(test_config.page_load_timeout)
    
    if test_config.headless:
        logger.info("Browser started in headless mode")
    else:
        driver.maximize_window()
        logger.info("Browser started in windowed mode")
    
    logger.test_data("Browser Configuration", {
        "browser": test_config.browser.value,
        "headless": test_config.headless,
        "window_size": test_config.window_size,
        "implicit_wait": test_config.implicit_wait
    })
    
    yield driver
    
    # Teardown - capture screenshot on failure
    if request.node.rep_call.failed and test_config.screenshot_on_failure:
        test_name = request.node.name
        screenshot_path = capture_screenshot(driver, test_name, reason="test_failure")
        
        # Attach to Allure report if available
        if screenshot_path:
            try:
                allure.attach.file(
                    screenshot_path,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass  # Allure not available or configured
    
    logger.info("Closing browser")
    driver.quit()


def _create_chrome_driver(config):
    """Create Chrome WebDriver with configured options"""
    chrome_options = Options()
    
    if config.headless:
        chrome_options.add_argument("--headless=new")
    
    chrome_options.add_argument(f"--window-size={config.window_size}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    # Performance optimizations
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    
    return webdriver.Chrome(options=chrome_options)


@pytest.fixture(scope="function")
def standard_user_credentials():
    """Provide standard user credentials"""
    return UserType.STANDARD


@pytest.fixture(scope="function")
def problem_user_credentials():
    """Provide problem user credentials"""
    return UserType.PROBLEM


@pytest.fixture(scope="function")
def invalid_user_credentials():
    """Provide invalid user credentials"""
    return UserType.INVALID


@pytest.fixture(scope="function")
def test_products():
    """Provide test product data"""
    from config import TestData
    return TestData.PRODUCT_NAMES[:3]  # First 3 products for testing


# PyTest hooks for better reporting
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results for failure handling
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_configure(config):
    """Configure pytest with custom markers and setup"""
    # Custom markers
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "user_management: tests related to user management"
    )
    config.addinivalue_line(
        "markers", "shopping_cart: tests related to shopping cart functionality"
    )
    config.addinivalue_line(
        "markers", "checkout: tests related to checkout process"
    )
    
    # Ensure directories exist
    Path("screenshots").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)


def pytest_sessionstart(session):
    """Session start hook"""
    logger = get_logger("TestSession")
    logger.info("🚀 Starting SauceDemo Test Suite 2.0")
    logger.test_data("Session Configuration", {
        "total_tests": session.testscollected,
        "config_file": "conftest.py",
        "framework": "pytest"
    })


def pytest_sessionfinish(session, exitstatus):
    """Session finish hook"""
    logger = get_logger("TestSession")
    
    # Calculate test results
    total = session.testscollected
    failed = session.testsfailed
    passed = total - failed
    
    logger.test_data("Session Results", {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "exit_status": exitstatus
    })
    
    if exitstatus == 0:
        logger.info("🎉 All tests completed successfully!")
    else:
        logger.warning(f"⚠️ Test session completed with failures. Exit status: {exitstatus}")


# Allure reporting fixtures and configuration
@pytest.fixture(autouse=True)
def allure_environment_setup(request):
    """Setup Allure environment information"""
    try:
        import allure
        config = get_config()
        
        # Add environment information to Allure report
        allure.dynamic.feature(request.module.__name__)
        allure.dynamic.story(request.function.__name__)
        
        # Add configuration as attachment
        config_info = f"""
        Browser: {config.browser.value}
        Headless: {config.headless}
        Base URL: {config.base_url}
        Timeout: {config.explicit_wait}s
        """
        
        allure.attach(
            config_info,
            name="Test Configuration",
            attachment_type=allure.attachment_type.TEXT
        )
        
    except ImportError:
        pass  # Allure not installed


@pytest.fixture
def allure_step_logger():
    """Provide Allure step logging capability"""
    class AllureStepLogger:
        @staticmethod
        def step(step_description: str):
            try:
                import allure
                return allure.step(step_description)
            except ImportError:
                # Fallback to context manager that does nothing
                from contextlib import nullcontext
                return nullcontext()
    
    return AllureStepLogger()