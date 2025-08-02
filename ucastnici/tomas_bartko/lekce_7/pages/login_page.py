from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """Login page object model"""
    
    # Locators
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password") 
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/"
    
    def open(self):
        """Navigate to login page"""
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.slowdown()
    
    def enter_username(self, username):
        """Enter username"""
        self.type_text(self.USERNAME_FIELD, username)
    
    def enter_password(self, password):
        """Enter password"""  
        self.type_text(self.PASSWORD_FIELD, password)
    
    def click_login(self):
        """Click login button"""
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """Complete login process"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def get_error_message(self):
        """Get error message text"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_element_text(self.ERROR_MESSAGE)
        return None
    
    def is_login_successful(self):
        """Check if login was successful by URL"""
        return "inventory.html" in self.get_current_url()
    
    def login_as_standard_user(self):
        """Quick login as standard user"""
        self.login("standard_user", "secret_sauce")
    
    def login_as_problem_user(self):
        """Quick login as problem user"""
        self.login("problem_user", "secret_sauce")
    
    def login_with_invalid_credentials(self):
        """Login with invalid credentials for testing"""
        self.login("invalid_user", "wrong_password")