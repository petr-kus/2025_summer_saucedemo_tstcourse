"""
Advanced Login Tests with PyTest and Domain Language
Comprehensive test coverage for login functionality
"""

import pytest
import allure
from pages.login_page import LoginPage
from config import UserType


@allure.epic("User Authentication")
@allure.feature("Login Functionality")
class TestLoginScenarios:
    """
    Comprehensive login test scenarios using advanced POM and domain language
    Each test is self-contained and follows best practices
    """
    
    @allure.story("Valid User Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.user_management
    def test_standard_user_successful_login(self, browser_driver, standard_user_credentials, allure_step_logger):
        """
        Test that standard user can successfully log in to the application
        
        This test verifies the happy path login flow for a standard user
        and ensures proper redirection to the inventory page.
        """
        login_page = LoginPage(browser_driver)
        
        with allure_step_logger.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure_step_logger.step(f"Login as {standard_user_credentials.name} user"):
            login_page.login_as_user_type(standard_user_credentials)
        
        with allure_step_logger.step("Verify successful login"):
            login_successful = login_page.verify_login_was_successful()
            assert login_successful, "Standard user should be able to login successfully"
    
    @allure.story("Problem User Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.user_management
    def test_problem_user_login_behavior(self, browser_driver, problem_user_credentials, allure_step_logger):
        """
        Test that problem user can log in (but may have issues later)
        
        This test verifies that the problem user can authenticate,
        even though they may encounter issues in subsequent operations.
        """
        login_page = LoginPage(browser_driver)
        
        with allure_step_logger.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure_step_logger.step(f"Login as {problem_user_credentials.name} user"):
            login_page.login_as_user_type(problem_user_credentials)
        
        with allure_step_logger.step("Verify login was successful"):
            login_successful = login_page.verify_login_was_successful()
            assert login_successful, "Problem user should be able to login (authentication works)"
    
    @allure.story("Invalid Credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.user_management
    def test_invalid_credentials_login_rejection(self, browser_driver, invalid_user_credentials, allure_step_logger):
        """
        Test that invalid credentials are properly rejected
        
        This test ensures the application properly handles and rejects
        invalid login attempts with appropriate error messaging.
        """
        login_page = LoginPage(browser_driver)
        
        with allure_step_logger.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure_step_logger.step(f"Attempt login with invalid credentials"):
            login_page.login_as_user_type(invalid_user_credentials)
        
        with allure_step_logger.step("Verify login was rejected"):
            login_failed = login_page.verify_login_failed()
            assert login_failed, "Invalid credentials should be rejected"
        
        with allure_step_logger.step("Verify appropriate error message"):
            error_correct = login_page.verify_specific_error_message("invalid_credentials")
            assert error_correct, "Should display correct error message for invalid credentials"
    
    @allure.story("Empty Credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.user_management
    def test_empty_username_validation(self, browser_driver, allure_step_logger):
        """
        Test validation for empty username field
        
        This test ensures proper validation when username is not provided.
        """
        login_page = LoginPage(browser_driver)
        
        with allure_step_logger.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure_step_logger.step("Attempt login with empty username"):
            login_page.enter_username("")
            login_page.enter_password("secret_sauce")
            login_page.click_login_button()
        
        with allure_step_logger.step("Verify login was rejected"):
            login_failed = login_page.verify_login_failed()
            assert login_failed, "Empty username should be rejected"
        
        with allure_step_logger.step("Verify appropriate error message"):
            error_correct = login_page.verify_specific_error_message("empty_username")
            assert error_correct, "Should display error message for empty username"
    
    @allure.story("Empty Credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.user_management
    def test_empty_password_validation(self, browser_driver, allure_step_logger):
        """
        Test validation for empty password field
        
        This test ensures proper validation when password is not provided.
        """
        login_page = LoginPage(browser_driver)
        
        with allure_step_logger.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure_step_logger.step("Attempt login with empty password"):
            login_page.enter_username("standard_user")
            login_page.enter_password("")
            login_page.click_login_button()
        
        with allure_step_logger.step("Verify login was rejected"):
            login_failed = login_page.verify_login_failed()
            assert login_failed, "Empty password should be rejected"
        
        with allure_step_logger.step("Verify appropriate error message"):
            error_correct = login_page.verify_specific_error_message("empty_password")
            assert error_correct, "Should display error message for empty password"
    
    @allure.story("Locked Out User")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.user_management
    def test_locked_out_user_rejection(self, browser_driver, allure_step_logger):
        """
        Test that locked out user is properly rejected
        
        This test verifies the application properly handles locked out users
        and displays appropriate error messaging.
        """
        login_page = LoginPage(browser_driver)
        
        with allure_step_logger.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure_step_logger.step("Attempt login as locked out user"):
            login_page.login_as_user_type(UserType.LOCKED_OUT)
        
        with allure_step_logger.step("Verify login was rejected"):
            login_failed = login_page.verify_login_failed()
            assert login_failed, "Locked out user should be rejected"
        
        with allure_step_logger.step("Verify appropriate error message"):
            error_correct = login_page.verify_specific_error_message("locked_out_user")
            assert error_correct, "Should display correct error message for locked out user"
    
    @allure.story("Login Form Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_form_elements_present(self, browser_driver, allure_step_logger):
        """
        Test that all login form elements are present and functional
        
        This test verifies the login form structure and element availability.
        """
        login_page = LoginPage(browser_driver)
        
        with allure_step_logger.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure_step_logger.step("Verify login page is properly displayed"):
            page_displayed = login_page.verify_login_page_is_displayed()
            assert page_displayed, "Login page should be properly displayed with all elements"
        
        with allure_step_logger.step("Test form field interactions"):
            # Test username field
            login_page.enter_username("test_user")
            login_page.clear_login_form()
            
            # Test password field
            login_page.enter_password("test_password")
            login_page.clear_login_form()
            
            # Test login button is clickable
            login_button_clickable = login_page.is_element_visible(login_page.LOGIN_BUTTON)
            assert login_button_clickable, "Login button should be visible and clickable"


@allure.epic("User Authentication")
@allure.feature("Login Integration") 
class TestLoginIntegrationScenarios:
    """
    Integration tests for login functionality with complete flows
    """
    
    @allure.story("Complete Login Flow")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_complete_successful_login_flow(self, browser_driver, standard_user_credentials):
        """
        Test complete login flow using the comprehensive method
        
        This integration test uses the complete login flow method
        to verify end-to-end login functionality.
        """
        login_page = LoginPage(browser_driver)
        
        # Use the comprehensive login flow method
        login_successful = login_page.perform_complete_valid_login_flow(standard_user_credentials)
        
        assert login_successful, "Complete login flow should succeed for valid user"
    
    @allure.story("Complete Invalid Login Flow")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_complete_invalid_login_flow(self, browser_driver):
        """
        Test complete invalid login flow using the comprehensive method
        
        This integration test uses the complete invalid login flow method
        to verify end-to-end error handling.
        """
        login_page = LoginPage(browser_driver)
        
        # Use the comprehensive invalid login flow method
        login_failed_correctly = login_page.perform_complete_invalid_login_flow("invalid_credentials")
        
        assert login_failed_correctly, "Complete invalid login flow should fail correctly with proper error"