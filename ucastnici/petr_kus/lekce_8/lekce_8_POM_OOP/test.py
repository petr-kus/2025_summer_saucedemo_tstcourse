from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
import time
logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

from saucedemo.LoginPage import LoginPage
from saucedemo.InventoryPage import InventoryPage
from saucedemo.Menu import Menu

#HANDY FUNCTIONS (low keywords)
def slowdown():
    time.sleep(2)

def log_test_fail(e):
        print(f"Test fail with error {e}")
        logging.error(f'Test fail with error. {e}')

#PRECONDITIONS
def open_browser_and_go_to(test_page):
    logging.info(f"Preparing browser chrome on page '{test_page}'...")
    driver = webdriver.Chrome()
    driver.get(test_page)
    logging.info(f"Browser chrome on '{test_page}' page PREPARED")
    return driver

#TEST CASES
def test_login_the_user(username,password):
    test_description = "This try to log a valid user and verify that user is correctly loged in."
    test_name = f"login user '{username}' '{password}'"
    test_passed = True
    try:
        logging.info(f'Testing {test_name} ...')
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        login_page.login_user(username,password)
        slowdown()
        inventory_page.we_are_on_page()

    except Exception as e:
        test_passed = False
        log_test_fail(e)

    finally: 
        if test_passed:
            logging.info(f'Test {test_name} PASSED')

def test_cart_badge_behavior():
    test_description = "This try to put random items to cart verify the number in badge and remove them all."
    test_name = "cart badge behavior"
    test_passed = True
    try:
        logging.info(f'Testing {test_name} ...')
        inventory_page = InventoryPage(driver)
        slowdown()
        inventory_page.add_random_products_to_cart()
        slowdown()
        inventory_page.remove_from_cart_all_products()
        slowdown()

    except Exception as e:
        test_passed = False
        log_test_fail(e)

    finally: 
        if test_passed:
            logging.info(f'Test {test_name} PASSED')

def test_logout_a_user():
    test_description = "This is try to logout user and verify that user is logged out."
    test_name = "logout user"
    test_passed = True
    try:
        logging.info(f'Testing {test_name} ...')
        menu_bar = Menu(driver)
        login_page = LoginPage(driver)
        menu_bar.open_menu()
        slowdown()
        menu_bar.press_logout()
        slowdown()
        login_page.we_are_on_page()

        #TODO: add better verification
        driver.find_element(By.ID, "login-button")
        
    except Exception as e:
        test_passed = False
        log_test_fail(e)

    finally: 
        if test_passed:
            logging.info(f'Test {test_name} PASSED')

def end_test():
    driver.quit()

#TEST SUITE / TEST EXECUTION
test_page = "https://www.saucedemo.com/"
username = "standard_user"
password = "secret_sauce"

global driver
driver = open_browser_and_go_to(test_page)

test_login_the_user(username,password)
test_cart_badge_behavior()
test_logout_a_user()
end_test()