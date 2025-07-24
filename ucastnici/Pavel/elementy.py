
from selenium.webdriver.common.by import By

class LoginPageLocators:
    USER_NAME_FIELD = (By.ID, 'user-name')
    PASSWORD_FIELD = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')

class InventoryPageLocators:
    PRODUCTS_HEADER = (By.CLASS_NAME, "title")
    ADD_TO_CART_BACKPACK_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")

class CartPageLocators:
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CHECKOUT_BUTTON = (By.ID, "checkout")

class CheckoutPageLocators:
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")  
    CONTINUE_BUTTON = (By.ID, "continue")