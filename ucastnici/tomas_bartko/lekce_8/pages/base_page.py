"""
Enhanced Base Page Object
Foundation for all page objects with advanced features
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Optional, Tuple

from utils import get_logger, capture_screenshot
from config import get_config


class BasePage:
    """
    Enhanced base page object with domain language methods
    Provides common functionality for all page objects
    """
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.config = get_config()
        self.wait = WebDriverWait(driver, self.config.explicit_wait)
        self.logger = get_logger(self.__class__.__name__)
        
        # Page identification
        self.page_url = ""
        self.page_title = ""
        self.unique_element = None  # Tuple of (By, locator) for page verification
    
    # =============================================================================
    # NAVIGATION DOMAIN LANGUAGE
    # =============================================================================
    
    def navigate_to_page(self) -> 'BasePage':
        """Navigate to this page"""
        if not self.page_url:
            raise NotImplementedError("page_url must be defined in child class")
        
        self.logger.test_action("Navigate to page", value=self.page_url)
        self.driver.get(self.page_url)
        self.wait_for_page_to_load()
        return self
    
    def wait_for_page_to_load(self) -> bool:
        """Wait for page to fully load using unique element"""
        if not self.unique_element:
            self.logger.warning("No unique element defined for page load verification")
            return True
        
        try:
            self.logger.test_action("Wait for page to load", element=str(self.unique_element))
            self.wait.until(EC.presence_of_element_located(self.unique_element))
            return True
        except TimeoutException:
            self.logger.error(f"Page failed to load within {self.config.explicit_wait} seconds")
            self.capture_failure_screenshot("page_load_timeout")
            return False
    
    def verify_page_is_displayed(self) -> bool:
        """Verify that the current page is displayed correctly"""
        try:
            # Check URL if defined
            if self.page_url:
                current_url = self.driver.current_url
                url_matches = self.page_url.lower() in current_url.lower()
                self.logger.test_verification(
                    "Page URL verification",
                    self.page_url,
                    current_url,
                    url_matches
                )
                if not url_matches:
                    return False
            
            # Check unique element if defined
            if self.unique_element:
                element_present = self.is_element_visible(self.unique_element)
                self.logger.test_verification(
                    "Page unique element visibility",
                    "Element visible",
                    f"Element {'visible' if element_present else 'not visible'}",
                    element_present
                )
                return element_present
            
            return True
        except Exception as e:
            self.logger.error(f"Page verification failed: {str(e)}")
            return False
    
    # =============================================================================
    # ELEMENT INTERACTION DOMAIN LANGUAGE
    # =============================================================================
    
    def find_clickable_element(self, locator: Tuple[By, str]) -> WebElement:
        """Find element that is clickable"""
        self.logger.test_action("Find clickable element", element=str(locator))
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            self.capture_failure_screenshot("element_not_clickable")
            raise
    
    def find_visible_element(self, locator: Tuple[By, str]) -> WebElement:
        """Find element that is visible"""
        self.logger.test_action("Find visible element", element=str(locator))
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible: {locator}")
            self.capture_failure_screenshot("element_not_visible")
            raise
    
    def find_present_element(self, locator: Tuple[By, str]) -> WebElement:
        """Find element that is present in DOM"""
        self.logger.test_action("Find present element", element=str(locator))
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Element not present: {locator}")
            self.capture_failure_screenshot("element_not_present")
            raise
    
    def find_all_visible_elements(self, locator: Tuple[By, str]) -> List[WebElement]:
        """Find all visible elements matching locator"""
        self.logger.test_action("Find all visible elements", element=str(locator))
        try:
            elements = self.wait.until(EC.visibility_of_all_elements_located(locator))
            self.logger.info(f"Found {len(elements)} visible elements")
            return elements
        except TimeoutException:
            self.logger.warning(f"No visible elements found: {locator}")
            return []
    
    def click_element_safely(self, locator: Tuple[By, str]) -> bool:
        """Click element with safety checks and logging"""
        try:
            element = self.find_clickable_element(locator)
            element_text = element.text[:50] if element.text else "No text"
            
            self.logger.test_action("Click element", element=str(locator), value=element_text)
            element.click()
            self.gentle_wait()
            return True
        except Exception as e:
            self.logger.error(f"Failed to click element {locator}: {str(e)}")
            self.capture_failure_screenshot("click_failed")
            return False
    
    def enter_text_safely(self, locator: Tuple[By, str], text: str, clear_first: bool = True) -> bool:
        """Enter text with safety checks and logging"""
        try:
            element = self.find_visible_element(locator)
            
            if clear_first:
                element.clear()
                self.logger.test_action("Clear field", element=str(locator))
            
            element.send_keys(text)
            self.logger.test_action("Enter text", element=str(locator), value=text)
            self.gentle_wait()
            return True
        except Exception as e:
            self.logger.error(f"Failed to enter text in {locator}: {str(e)}")
            self.capture_failure_screenshot("text_entry_failed")
            return False
    
    def get_element_text_safely(self, locator: Tuple[By, str]) -> str:
        """Get element text with safety checks"""
        try:
            element = self.find_visible_element(locator)
            text = element.text
            self.logger.test_action("Get element text", element=str(locator), value=text)
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text from {locator}: {str(e)}")
            return ""
    
    def is_element_visible(self, locator: Tuple[By, str]) -> bool:
        """Check if element is visible without waiting"""
        try:
            element = self.driver.find_element(*locator)
            is_visible = element.is_displayed()
            self.logger.debug(f"Element {locator} visibility: {is_visible}")
            return is_visible
        except NoSuchElementException:
            self.logger.debug(f"Element {locator} not found in DOM")
            return False
    
    def is_element_present(self, locator: Tuple[By, str]) -> bool:
        """Check if element is present in DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    # =============================================================================
    # WAITING AND TIMING DOMAIN LANGUAGE
    # =============================================================================
    
    def gentle_wait(self, seconds: float = 0.5):
        """Short wait for UI stability"""
        time.sleep(seconds)
    
    def wait_for_element_to_disappear(self, locator: Tuple[By, str], timeout: int = 5) -> bool:
        """Wait for element to disappear from DOM"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until_not(EC.presence_of_element_located(locator))
            self.logger.test_action("Wait for element to disappear", element=str(locator))
            return True
        except TimeoutException:
            self.logger.warning(f"Element did not disappear: {locator}")
            return False
    
    def wait_for_text_to_change(self, locator: Tuple[By, str], old_text: str, timeout: int = 5) -> bool:
        """Wait for element text to change from old_text"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until_not(EC.text_to_be_present_in_element(locator, old_text))
            return True
        except TimeoutException:
            return False
    
    # =============================================================================
    # VERIFICATION DOMAIN LANGUAGE
    # =============================================================================
    
    def verify_element_contains_text(self, locator: Tuple[By, str], expected_text: str) -> bool:
        """Verify element contains expected text"""
        actual_text = self.get_element_text_safely(locator)
        contains_text = expected_text.lower() in actual_text.lower()
        
        self.logger.test_verification(
            f"Element contains text",
            expected_text,
            actual_text,
            contains_text
        )
        
        if not contains_text:
            self.capture_failure_screenshot("text_verification_failed")
        
        return contains_text
    
    def verify_element_has_exact_text(self, locator: Tuple[By, str], expected_text: str) -> bool:
        """Verify element has exact text"""
        actual_text = self.get_element_text_safely(locator)
        exact_match = expected_text == actual_text
        
        self.logger.test_verification(
            f"Element has exact text",
            expected_text,
            actual_text,
            exact_match
        )
        
        if not exact_match:
            self.capture_failure_screenshot("exact_text_verification_failed")
        
        return exact_match
    
    def verify_current_url_contains(self, expected_url_part: str) -> bool:
        """Verify current URL contains expected part"""
        current_url = self.driver.current_url
        contains_url = expected_url_part.lower() in current_url.lower()
        
        self.logger.test_verification(
            "URL contains expected part",
            expected_url_part,
            current_url,
            contains_url
        )
        
        return contains_url
    
    # =============================================================================
    # SCREENSHOT AND DEBUGGING DOMAIN LANGUAGE
    # =============================================================================
    
    def capture_page_screenshot(self, reason: str = "") -> str:
        """Capture screenshot of current page"""
        test_name = self.__class__.__name__
        return capture_screenshot(self.driver, test_name, reason=reason)
    
    def capture_failure_screenshot(self, failure_reason: str) -> str:
        """Capture screenshot on failure"""
        test_name = self.__class__.__name__
        return capture_screenshot(self.driver, test_name, failure_reason, "failure")
    
    def log_page_info(self):
        """Log current page information for debugging"""
        info = {
            "url": self.driver.current_url,
            "title": self.driver.title,
            "window_size": self.driver.get_window_size()
        }
        self.logger.test_data("Current Page Info", info)
    
    # =============================================================================
    # BROWSER CONTROL DOMAIN LANGUAGE
    # =============================================================================
    
    def refresh_page(self):
        """Refresh current page"""
        self.logger.test_action("Refresh page")
        self.driver.refresh()
        self.wait_for_page_to_load()
    
    def maximize_browser_window(self):
        """Maximize browser window"""
        self.logger.test_action("Maximize browser window")
        self.driver.maximize_window()
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get current page title"""
        return self.driver.title