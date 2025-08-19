from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from login_page import LoginPage
from inventory_page import InventoryPage
import pytest
import logging

logger = logging.getLogger(__name__)
logging .basicConfig(filename="loggy.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

eshop_url = "https://www.saucedemo.com/"
user = {"name": "standard_user", "password": "secret_sauce"}

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login(driver):
    login_page = LoginPage(driver)
    login_page.go_to_page()
    login_page.login(user["name"], user["password"])
    
    logger.info("Přihlášení proběhlo úspěšně.")
    
    assert login_page.is_login_successful(), "Přihlášení selhalo"
    return InventoryPage(driver)

def test_add_to_cart(login):
    inventory_page = login
    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    cart_page = inventory_page.open_cart()

    assert cart_page.is_item_in_cart("Sauce Labs Backpack"), "Produkt není v košíku"

def test_checkout_complete(login):
    inventory_page = login
    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    cart_page = inventory_page.open_cart()
    checkout_page = cart_page.click_checkout()
    assert checkout_page is not None, "Nepodařilo se otevřít checkout stránku"

    checkout_page.enter_checkout_information("Pavel", "Petrle", "12345")
    checkout_page.click_continue()

    checkout_page.click_finish()
    assert checkout_page.is_checkout_complete(), "Objednávka nebyla dokončena"