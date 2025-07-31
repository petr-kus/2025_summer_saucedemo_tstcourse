from pages.base_page import BasePage
from elementy import CartPageLocators, CheckoutPageLocators

class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, url="https://www.saucedemo.com/cart.html")
        self.locators = CartPageLocators
        self.checkout_locators = CheckoutPageLocators

    def is_item_in_cart(self, item_name):
        """Ověří, zda je daná položka v košíku."""
        elements = self.driver.find_elements(*self.locators.CART_ITEM_NAME)
        return any(item_name in el.text for el in elements)

    def click_checkout(self):
        """Klikne na tlačítko 'Checkout'."""
        if self.click_element(self.checkout_locators.CHECKOUT_BUTTON, "Tlačítko Checkout"):
            from pages.checkout_page import CheckoutPage
            return CheckoutPage(self.driver)
        return None

class CartPageLocators:
    CART_ITEM_NAME = ("xpath", "//div[@class='inventory_item_name']")
    

#class CartPage(BasePage):
    #def __init__(self, driver):
       # super().__init__(driver, url="https://www.saucedemo.com/cart.html")
      #  self.locators = CartPageLocators
       #self.checkout_locators = CheckoutPageLocators
    def open_cart(self):
        """Otevře košík."""
        self.click_element(self.locators.SHOPPING_CART_LINK, "Otevření košíku")
        from pages.cart_page import CartPage
        return CartPage(self.driver)

    def is_item_in_cart(self, item_name):
        """Ověří, zda je daná položka v košíku."""
        locator = self.locators.CART_ITEM_NAME(item_name)
        return self.is_element_displayed(locator, f"Položka '{item_name}' v košíku")