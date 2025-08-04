import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from page.log_page import Page_Logging
from page.inventory_page import Page_Inventory
from page.cart_page import Page_Cart
from setup_8 import logger, url

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_driver(driver):
    login_page = Page_Logging(driver, logger, url)
    login_page.login_user("standard_user", "secret_sauce")
    return driver

def test_login(driver):
    login_page = Page_Logging(driver, logger=logger, url=url)
    login_page.login_user("standard_user", "secret_sauce")

@pytest.mark.parametrize("name, button_add, button_remove, text", [
    (
        "batoh",
        (By.ID, "add-to-cart-sauce-labs-backpack"),
        (By.ID, "remove-sauce-labs-backpack"),
        "Sauce Labs Backpack"
    ),
    (
        "tricko",
        (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"),
        (By.ID, "remove-sauce-labs-bolt-t-shirt"),
        "Sauce Labs Bolt T-Shirt"
    ),
    (
        "bunda",
        (By.ID, "add-to-cart-sauce-labs-fleece-jacket"),
        (By.ID, "remove-sauce-labs-fleece-jacket"),
        "Sauce Labs Fleece Jacket"
    ),
    (
        "svetlo",
        (By.ID, "add-to-cart-sauce-labs-bike-light"),
        (By.ID, "remove-sauce-labs-bike-light"),
        "Sauce Labs Bike Light"
    )
])

def test_cart(logged_in_driver, name, button_add, button_remove, text):
    driver = logged_in_driver
    try:
        product = Page_Inventory(
            driver=driver,
            logger=logger,
            name=name,
            button_add=button_add,
            button_remove=button_remove,
            text=text
        )
        product.add_to_cart()
        cart = Page_Cart(driver, logger)
        cart.open_cart_from_inventory()
        cart.assert_item_in_cart(text)
        cart.return_to_inventory_from_cart()
        product.remove_from_cart()
        cart.open_cart_from_inventory()
        cart.assert_item_not_in_cart(text)
        cart.return_to_inventory_from_cart()
    except Exception as e:
        logger.error(f"Chyba při testu košíku: {e}")
        raise

