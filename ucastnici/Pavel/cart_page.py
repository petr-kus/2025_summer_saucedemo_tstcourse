from selenium.webdriver.common.by import By
from checkout_page import CheckoutPage
import logging

logger = logging.getLogger(__name__)

class CartPage:
    
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
    
    def is_item_in_cart(self, item_name):
        locator = (By.XPATH, f"//div[@class='inventory_item_name' and text()='{item_name}']")
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    def click_checkout(self):

        self.driver.find_element(*self.CHECKOUT_BUTTON).click()
        logger.info("Clicked checkout button.")
        return CheckoutPage(self.driver)