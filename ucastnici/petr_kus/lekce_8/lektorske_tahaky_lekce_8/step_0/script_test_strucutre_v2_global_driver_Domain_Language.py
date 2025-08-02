from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import logging
import time
logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

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
        slowdown()
        logging.info(f"Testing {test_name} ...")
        field_username = driver.find_element(By.ID, "user-name")
        field_username.send_keys(username)
        slowdown()
        field_password = driver.find_element(By.ID, "password")
        field_password.send_keys(password)
        slowdown()
        button_submit = driver.find_element(By.ID, "login-button")
        button_submit.click()
        slowdown()
        assert "inventory" in driver.current_url, f"Expected 'inventory' in url, but in url '{driver.current_url}' was not found."

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
    add_to_cart_button = (By.XPATH, "//button[text()='Add to cart']")
    remove_from_cart_button = (By.XPATH, "//button[text()='Remove']")
    cart_badge = (By.CLASS_NAME, "shopping_cart_badge")

    try:
        logging.info(f'Testing {test_name} ...')
        add_to_cart_buttons = driver.find_elements(*add_to_cart_button)
        num_to_add = random.randint(1, len(add_to_cart_buttons))
        buttons_to_add = random.sample(add_to_cart_buttons, num_to_add)
        
        logging.debug(f"Was selected  '{num_to_add}' items to add to cart.")

        for button in buttons_to_add:
            slowdown()
            button.click()
            logging.debug(f"Item '{button}' was added to cart.")

        time.sleep(0.5)
        cart_count = int(driver.find_element(*cart_badge).text)
        assert cart_count == num_to_add, f"Expected '{num_to_add}' items, but found '{cart_count}' in cart."

        remove_from_cart_buttons = driver.find_elements(*remove_from_cart_button)
        assert len(remove_from_cart_buttons) == cart_count, f"Expected '{cart_count}' remove buttons, but found '{len(remove_from_cart_buttons)}' remove buttons."

        for button in remove_from_cart_buttons:
            slowdown()
            button.click()
            cart_count = cart_count-1
            time.sleep(0.5)
            if not cart_count == 0:
                current_cart_count = int(driver.find_element(*cart_badge).text)
                assert cart_count == current_cart_count, f"Expected '{cart_count}' items, but found '{current_cart_count}' in cart."
            else:
                cart_badge_elements = driver.find_elements(*cart_badge)
                assert len(cart_badge_elements) == 0, "Cart badge is still visible after removing all items!"
            logging.debug(f"Item  '{button}' was correctly removed from the cart.")

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
    main_menu_button = (By.ID, "react-burger-menu-btn")
    logout_button = (By.XPATH,"//nav/*[text()='Logout']")
    try:
        slowdown()
        logging.info(f'Testing {test_name} ...')
        slowdown()
        driver.find_element(*main_menu_button).click()
        slowdown()
        WebDriverWait(driver,2).until(EC.visibility_of_element_located(logout_button)).click()
        slowdown()
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