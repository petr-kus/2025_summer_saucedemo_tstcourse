from pages.base_page import BasePage
from elementy import InventoryPageLocators, CartPageLocators
import logging

class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, url="https://www.saucedemo.com/inventory.html")
        self.locators = InventoryPageLocators
        self.cart_locators = CartPageLocators

    def add_item_to_cart(self, item_name):
        if item_name == "Sauce Labs Backpack":
            self.click_element(self.locators.ADD_TO_CART_BACKPACK_BUTTON, f"Přidání '{item_name}' do košíku")
        else:
            logging.warning(f"Položka '{item_name}' není definována pro přidání do košíku v InventoryPage.")

    def open_cart(self):
        self.click_element(self.cart_locators.SHOPPING_CART_LINK, "Otevření košíku")
        from pages.cart_page import CartPage
        return CartPage(self.driver)

    def is_products_page_displayed(self):
        header_text = self.get_element_text(self.locators.PRODUCTS_HEADER, "Nadpis stránky Products")
        return header_text == "Products"