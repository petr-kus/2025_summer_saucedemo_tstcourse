from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def slowdown(self, seconds=2):
        """Helper method for delays"""
        time.sleep(seconds)
    
    def find_element(self, locator):
        """Find element with wait"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """Find multiple elements"""
        return self.driver.find_elements(*locator)
    
    def click_element(self, locator):
        """Click element with wait"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        self.slowdown(0.5)
    
    def type_text(self, locator, text):
        """Type text into element"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        self.slowdown(0.5)
    
    def get_element_text(self, locator):
        """Get text from element"""
        return self.find_element(locator).text
    
    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except:
            return False
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url