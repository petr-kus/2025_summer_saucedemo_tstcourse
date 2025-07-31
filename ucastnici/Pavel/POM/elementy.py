
from selenium.webdriver.common.by import By

class LoginPageLocators:
    #USER_NAME_FIELD = (By.XPATH, "//*[@id='user-name']" and "[@name='user-name']")
    #PASSWORD_FIELD = (By.XPATH, "//*[@id='password', @name='password']")
    #LOGIN_BUTTON = (By.XPATH, "//*[@value='login-button'][@type='submit']")
    USER_NAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

class InventoryPageLocators:
    PRODUCTS_HEADER = (By.CLASS_NAME, "title")
    ADD_TO_CART_BACKPACK_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")

class CartPageLocators:
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_ITEM_NAME = lambda item_name: (By.XPATH, f"//div[@class='inventory_item_name' and text()='{item_name}']")


class CheckoutPageLocators:
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")  
    CONTINUE_BUTTON = (By.ID, "continue")
    CHECKOUT_BUTTON = ("id", "checkout")
    FIRST_NAME_FIELD = ("id", "first-name")
    LAST_NAME_FIELD = ("id", "last-name")
    ZIP_POSTAL_CODE_FIELD = ("id", "postal-code")
    CONTINUE_BUTTON = ("id", "continue")
    FINISH_BUTTON = ("id", "finish")
    CHECKOUT_COMPLETE_HEADER = ("class name", "complete-header")
    
    