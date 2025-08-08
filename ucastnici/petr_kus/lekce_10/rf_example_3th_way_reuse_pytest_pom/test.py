from selenium import webdriver
import time
from saucedemo.LoginPage import LoginPage
from saucedemo.InventoryPage import InventoryPage
from saucedemo.Menu import Menu
import pytest

test_page = "https://www.saucedemo.com/"
my_username = "standard_user"
my_password = "secret_sauce"

@pytest.fixture(autouse=True, scope="session")
def Browser():
    global browser
    browser = webdriver.Chrome()
    browser.get("https://www.saucedemo.com/")
    yield browser
    browser.quit()

@pytest.fixture
def username():
    return my_username

@pytest.fixture
def password():
    return my_password

#HANDY FUNCTIONS (low keywords)
def slowdown():
    time.sleep(2)

#TEST CASES
def test_login_the_user(username,password):
    """This try to log a valid user and verify that user is correctly loged in."""
    login_page = LoginPage(browser)
    inventory_page = InventoryPage(browser)
    login_page.login_user(username,password)
    slowdown()
    inventory_page.we_are_on_page()

def test_cart_badge_behavior():
    """This try to put random items to cart verify the number in badge and remove them all."""
    inventory_page = InventoryPage(browser)
    slowdown()
    inventory_page.add_random_products_to_cart()
    slowdown()
    inventory_page.remove_from_cart_all_products()
    slowdown()

def test_logout_a_user():
    """This is try to logout user and verify that user is logged out."""
    menu_bar = Menu(browser)
    login_page = LoginPage(browser)
    menu_bar.open_menu()
    slowdown()
    menu_bar.press_logout()
    slowdown()
    login_page.we_are_on_page()