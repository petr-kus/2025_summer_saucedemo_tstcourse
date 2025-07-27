from selenium.webdriver.common.by import By
import random
import logging
import time

class InventoryPage:
    add_to_cart_button = (By.XPATH, "//button[text()='Add to cart']")
    remove_from_cart_button = (By.XPATH, "//button[text()='Remove']")
    cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
    page_url = "inventory"

    def __init__(self, driver):
        self.driver = driver

    def we_are_on_page(self):
        assert self.page_url in self.driver.current_url

    def add_product_to_cart(self,add_button):
        add_button.click()

    def remove_product_from_cart(self,remove_button):
        remove_button.click()
    
    def add_random_products_to_cart(self):
        add_to_cart_buttons = self.driver.find_elements(*self.add_to_cart_button)
        num_to_add = random.randint(1, len(add_to_cart_buttons))
        buttons_to_add = random.sample(add_to_cart_buttons, num_to_add)

        for button in buttons_to_add:
            self.add_product_to_cart(button)
            logging.debug(f"Item '{button}' was added to cart.")

        time.sleep(0.5)
        cart_count = int(self.driver.find_element(*self.cart_badge).text)
        assert cart_count == num_to_add, f"Expected '{num_to_add}' items, but found '{cart_count}' in cart."

    def remove_from_cart_all_products(self):
        cart_count = int(self.driver.find_element(*self.cart_badge).text)
        remove_from_cart_buttons = self.driver.find_elements(*self.remove_from_cart_button)
        assert len(remove_from_cart_buttons) == cart_count, f"Expected '{cart_count}' remove buttons, but found '{len(remove_from_cart_buttons)}' remove buttons."

        for button in remove_from_cart_buttons:
            button.click()
            cart_count = cart_count-1
            time.sleep(0.5)
            if not cart_count == 0:
                current_cart_count = int(self.driver.find_element(*self.cart_badge).text)
                assert cart_count == current_cart_count, f"Expected '{cart_count}' items, but found '{current_cart_count}' in cart."
            else:
                cart_badge_elements = self.driver.find_elements(*self.cart_badge)
                assert len(cart_badge_elements) == 0, "Cart badge is still visible after removing all items!"
            logging.debug(f"Item  '{button}' was correctly removed from the cart.")
            
