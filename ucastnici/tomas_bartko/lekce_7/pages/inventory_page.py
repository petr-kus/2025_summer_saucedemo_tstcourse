from selenium.webdriver.common.by import By
from .base_page import BasePage


class InventoryPage(BasePage):
    """Inventory/Products page object model"""
    
    # Locators
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    INVENTORY_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[class*='btn_inventory']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_page_loaded(self):
        """Check if inventory page is loaded"""
        return "inventory.html" in self.get_current_url() and \
               self.is_element_visible(self.INVENTORY_LIST)
    
    def get_all_products(self):
        """Get all product elements"""
        return self.find_elements(self.INVENTORY_ITEMS)
    
    def get_all_add_to_cart_buttons(self):
        """Get all add to cart buttons"""
        return self.find_elements(self.ADD_TO_CART_BUTTONS)
    
    def get_product_name(self, product_element):
        """Get product name from product element"""
        return product_element.find_element(*self.INVENTORY_ITEM_NAME).text
    
    def add_product_to_cart_by_name(self, product_name):
        """Add specific product to cart by name"""
        products = self.get_all_products()
        
        for product in products:
            if self.get_product_name(product) == product_name:
                button = product.find_element(By.CSS_SELECTOR, "button[class*='btn_inventory']")
                if button.text == "Add to cart":
                    button.click()
                    self.slowdown()
                    # Debug: check if button changed to Remove
                    button_after = product.find_element(By.CSS_SELECTOR, "button[class*='btn_inventory']")
                    print(f"  Debug: Button changed from 'Add to cart' to '{button_after.text}'")
                    return True
        return False
    
    def add_first_n_products_to_cart(self, count=3):
        """Add first N products to cart"""
        buttons = self.get_all_add_to_cart_buttons()
        products_added = []
        
        for i, button in enumerate(buttons[:count]):
            if button.text == "Add to cart":
                # Get product name
                inventory_item = button.find_element(By.XPATH, "../../..")
                product_name = inventory_item.find_element(*self.INVENTORY_ITEM_NAME).text
                
                button.click()
                self.slowdown()
                products_added.append(product_name)
        
        return products_added
    
    def get_cart_item_count(self):
        """Get number of items in cart from badge"""
        try:
            badge = self.find_element(self.CART_BADGE)
            return int(badge.text)
        except:
            return 0
    
    def go_to_cart(self):
        """Navigate to cart page"""
        self.click_element(self.CART_LINK)
    
    def is_product_added_to_cart(self, product_name):
        """Check if specific product shows 'Remove' button"""
        products = self.get_all_products()
        
        for product in products:
            if self.get_product_name(product) == product_name:
                button = product.find_element(By.CSS_SELECTOR, "button[class*='btn_inventory']")
                return button.text == "Remove"
        return False
    
    def get_all_product_names(self):
        """Get names of all available products"""
        products = self.get_all_products()
        return [self.get_product_name(product) for product in products]