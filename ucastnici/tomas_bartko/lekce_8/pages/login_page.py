"""
Enhanced Login Page Object
Provides domain language methods for login functionality
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Optional

from .base_page import BasePage
from config import UserType, get_config, TestData


class LoginPage(BasePage):
    """
    Login page object with enhanced domain language methods
    Handles all login-related functionality with comprehensive logging
    """
    
    # Page identification
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.page_url = get_config().base_url
        self.page_title = "Swag Labs"
        self.unique_element = self.LOGIN_BUTTON
    
    # =============================================================================
    # LOCATORS - Well-named and organized
    # =============================================================================
    
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password") 
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_BUTTON = (By.CSS_SELECTOR, "[data-test='error'] button")
    
    # Visual elements for comprehensive verification
    LOGIN_LOGO = (By.CLASS_NAME, "login_logo")
    LOGIN_FORM = (By.ID, "login_button_container")
    
    # =============================================================================
    # NAVIGATION DOMAIN LANGUAGE
    # =============================================================================
    
    def navigate_to_login_page(self) -> 'LoginPage':
        """Navigate to login page and verify it loaded"""
        self.logger.test_step("Navigate to SauceDemo login page")
        self.navigate_to_page()
        self.maximize_browser_window()
        
        # Verify login page is displayed
        if not self.verify_login_page_is_displayed():
            raise Exception("Login page failed to load properly")
        
        return self
    
    def verify_login_page_is_displayed(self) -> bool:
        """Verify login page is properly displayed"""
        self.logger.test_step("Verify login page is displayed")
        
        # Check page URL
        url_correct = self.verify_current_url_contains("saucedemo.com")
        
        # Check login form is visible
        form_visible = self.is_element_visible(self.LOGIN_FORM)
        
        # Check login button is present
        button_present = self.is_element_present(self.LOGIN_BUTTON)
        
        all_checks_passed = url_correct and form_visible and button_present
        
        self.logger.test_verification(
            "Login page verification",
            "All elements present and visible",
            f"URL: {url_correct}, Form: {form_visible}, Button: {button_present}",
            all_checks_passed
        )
        
        return all_checks_passed
    
    # =============================================================================
    # CREDENTIAL INPUT DOMAIN LANGUAGE
    # =============================================================================
    
    def enter_username(self, username: str) -> 'LoginPage':
        """Enter username with validation and logging"""
        self.logger.test_step(f"Enter username", username=username)
        
        if not username:
            self.logger.warning("Empty username provided")
        
        success = self.enter_text_safely(self.USERNAME_INPUT, username, clear_first=True)
        if not success:
            raise Exception(f"Failed to enter username: {username}")
        
        return self
    
    def enter_password(self, password: str) -> 'LoginPage':
        """Enter password with validation and logging"""
        self.logger.test_step("Enter password", password="***masked***")
        
        if not password:
            self.logger.warning("Empty password provided")
        
        success = self.enter_text_safely(self.PASSWORD_INPUT, password, clear_first=True)
        if not success:
            raise Exception("Failed to enter password")
        
        return self
    
    def clear_login_form(self) -> 'LoginPage':
        """Clear both username and password fields"""
        self.logger.test_step("Clear login form")
        
        # Clear username
        self.enter_text_safely(self.USERNAME_INPUT, "", clear_first=True)
        
        # Clear password  
        self.enter_text_safely(self.PASSWORD_INPUT, "", clear_first=True)
        
        return self
    
    # =============================================================================
    # LOGIN ACTION DOMAIN LANGUAGE
    # =============================================================================
    
    def click_login_button(self) -> 'LoginPage':
        """Click login button and wait for response"""
        self.logger.test_step("Click login button")
        
        success = self.click_element_safely(self.LOGIN_BUTTON)
        if not success:
            raise Exception("Failed to click login button")
        
        # Wait a moment for page response
        self.gentle_wait(1.0)
        
        return self
    
    def perform_login_with_credentials(self, username: str, password: str) -> 'LoginPage':
        """Complete login flow with provided credentials"""
        self.logger.test_step(f"Perform login", username=username, password="***masked***")
        
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
        return self
    
    def login_as_user_type(self, user_type: UserType) -> 'LoginPage':
        """Login using predefined user type"""
        self.logger.test_step(f"Login as {user_type.name} user", username=user_type.username)
        
        return self.perform_login_with_credentials(user_type.username, user_type.password)
    
    def login_as_standard_user(self) -> 'LoginPage':
        """Quick method to login as standard user"""
        return self.login_as_user_type(UserType.STANDARD)
    
    def login_as_problem_user(self) -> 'LoginPage':
        """Quick method to login as problem user"""
        return self.login_as_user_type(UserType.PROBLEM)
    
    def login_as_invalid_user(self) -> 'LoginPage':
        """Quick method to attempt login with invalid credentials"""
        return self.login_as_user_type(UserType.INVALID)
    
    # =============================================================================
    # LOGIN VERIFICATION DOMAIN LANGUAGE
    # =============================================================================
    
    def verify_login_was_successful(self) -> bool:
        """Verify that login succeeded by checking URL change"""
        self.logger.test_step("Verify login was successful")
        
        # Check if we're redirected to inventory page
        url_changed = self.verify_current_url_contains("inventory.html")
        
        # Additional check - login form should not be visible anymore
        login_form_gone = not self.is_element_visible(self.LOGIN_FORM)
        
        success = url_changed and login_form_gone
        
        self.logger.test_verification(
            "Login success verification",
            "Redirected to inventory page",
            f"URL changed: {url_changed}, Form gone: {login_form_gone}",
            success
        )
        
        if success:
            self.logger.info("✅ Login successful - user authenticated")
        else:
            self.capture_failure_screenshot("login_verification_failed")
        
        return success
    
    def verify_login_failed(self) -> bool:
        """Verify that login attempt failed"""
        self.logger.test_step("Verify login failed")
        
        # Check that we're still on login page
        still_on_login = not self.verify_current_url_contains("inventory.html")
        
        # Check if error message is displayed
        error_displayed = self.is_error_message_displayed()
        
        failed_as_expected = still_on_login and error_displayed
        
        self.logger.test_verification(
            "Login failure verification",
            "Still on login page with error",
            f"On login page: {still_on_login}, Error shown: {error_displayed}",
            failed_as_expected
        )
        
        return failed_as_expected
    
    # =============================================================================
    # ERROR HANDLING DOMAIN LANGUAGE
    # =============================================================================
    
    def is_error_message_displayed(self) -> bool:
        """Check if any error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE_CONTAINER)
    
    def get_error_message_text(self) -> str:
        """Get the current error message text"""
        self.logger.test_step("Get error message text")
        
        if not self.is_error_message_displayed():
            self.logger.warning("No error message is displayed")
            return ""
        
        error_text = self.get_element_text_safely(self.ERROR_MESSAGE_CONTAINER)
        self.logger.test_data("Error Message", {"text": error_text})
        
        return error_text
    
    def verify_error_message_contains(self, expected_text: str) -> bool:
        """Verify error message contains expected text"""
        self.logger.test_step(f"Verify error message contains: {expected_text}")
        
        if not self.is_error_message_displayed():
            self.logger.error("No error message displayed to verify")
            return False
        
        return self.verify_element_contains_text(self.ERROR_MESSAGE_CONTAINER, expected_text)
    
    def verify_specific_error_message(self, error_type: str) -> bool:
        """Verify specific error message by type"""
        expected_messages = TestData.ERROR_MESSAGES
        
        if error_type not in expected_messages:
            self.logger.error(f"Unknown error type: {error_type}")
            return False
        
        expected_text = expected_messages[error_type]
        return self.verify_error_message_contains(expected_text)
    
    def dismiss_error_message(self) -> 'LoginPage':
        """Dismiss error message by clicking X button"""
        self.logger.test_step("Dismiss error message")
        
        if not self.is_error_message_displayed():
            self.logger.warning("No error message to dismiss")
            return self
        
        success = self.click_element_safely(self.ERROR_CLOSE_BUTTON)
        if success:
            # Wait for error to disappear
            self.wait_for_element_to_disappear(self.ERROR_MESSAGE_CONTAINER)
        
        return self
    
    # =============================================================================
    # COMPREHENSIVE TEST SCENARIOS
    # =============================================================================
    
    def perform_complete_valid_login_flow(self, user_type: UserType = UserType.STANDARD) -> bool:
        """
        Complete login flow with verification
        Returns True if login successful, False otherwise
        """
        self.logger.test_step(f"Complete login flow for {user_type.name}")
        
        try:
            self.navigate_to_login_page()
            self.login_as_user_type(user_type)
            return self.verify_login_was_successful()
        except Exception as e:
            self.logger.error(f"Login flow failed: {str(e)}")
            self.capture_failure_screenshot("complete_login_flow_failed")
            return False
    
    def perform_complete_invalid_login_flow(self, expected_error_type: str = "invalid_credentials") -> bool:
        """
        Complete invalid login flow with error verification
        Returns True if login failed as expected, False otherwise
        """
        self.logger.test_step(f"Complete invalid login flow expecting: {expected_error_type}")
        
        try:
            self.navigate_to_login_page()
            self.login_as_invalid_user()
            
            # Verify login failed
            login_failed = self.verify_login_failed()
            
            # Verify specific error message
            error_correct = self.verify_specific_error_message(expected_error_type)
            
            return login_failed and error_correct
            
        except Exception as e:
            self.logger.error(f"Invalid login flow failed: {str(e)}")
            self.capture_failure_screenshot("invalid_login_flow_failed")
            return False