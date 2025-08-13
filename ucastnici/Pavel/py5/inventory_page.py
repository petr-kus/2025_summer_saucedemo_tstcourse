from selenium.webdriver.common.by import By
from cart_page import CartPage
import logging

class InventoryPage:
    
    PRODUCTS_HEADER = (By.CLASS_NAME, "title")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver

    def add_item_to_cart(self, item_name):
        locator = (By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item_label']/following-sibling::div/button")
        self.driver.find_element(*locator).click()
        logging.info(f"Item '{item_name}' added to cart.")

    def open_cart(self):
        self.driver.find_element(*self.SHOPPING_CART_LINK).click()
        logging.info("Otevírám košík.")
        return CartPage(self.driver)