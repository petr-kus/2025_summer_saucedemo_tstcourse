from selenium.webdriver.common.by import By
from .base_page import BasePage


class CartPage(BasePage):
    """Shopping cart page object model"""
    
    # Locators
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[class*='cart_button']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_page_loaded(self):
        """Check if cart page is loaded"""
        return "cart.html" in self.get_current_url()
    
    def get_cart_items(self):
        """Get all items in cart"""
        return self.find_elements(self.CART_ITEMS)
    
    def get_cart_item_count(self):
        """Get number of items in cart"""
        return len(self.get_cart_items())
    
    def get_cart_item_names(self):
        """Get names of all items in cart"""
        items = self.get_cart_items()
        names = []
        
        for item in items:
            name_element = item.find_element(*self.CART_ITEM_NAMES)
            names.append(name_element.text)
        
        return names
    
    def is_checkout_button_visible(self):
        """Check if checkout button is visible"""
        return self.is_element_visible(self.CHECKOUT_BUTTON)
    
    def click_checkout(self):
        """Click checkout button"""
        self.click_element(self.CHECKOUT_BUTTON)
    
    def continue_shopping(self):
        """Continue shopping - go back to inventory"""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
    
    def remove_item_by_name(self, product_name):
        """Remove specific item from cart"""
        items = self.get_cart_items()
        
        for item in items:
            name_element = item.find_element(*self.CART_ITEM_NAMES)
            if name_element.text == product_name:
                remove_button = item.find_element(By.CSS_SELECTOR, "button[class*='cart_button']")
                remove_button.click()
                self.slowdown()
                return True
        return False
    
    def is_cart_empty(self):
        """Check if cart is empty"""
        return self.get_cart_item_count() == 0