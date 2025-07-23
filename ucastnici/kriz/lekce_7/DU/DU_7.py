from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

#testovaci data
eshop = "https://www.saucedemo.com/"

test_users = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "locked_out": {"username": "locked_out_user", "password": "secret_sauce"},
    "problem": {"username": "problem_user", "password": "secret_sauce"},
    "performance_glitch": {"username": "performance_glitch_user", "password": "secret_sauce"},
    "error": {"username": "error_user", "password": "secret_sauce"},
    "visual": {"username": "visual_user", "password": "secret_sauce"}
}

goods = {
    "batoh": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-backpack"),
        "button_remove": (By.ID, "remove-sauce-labs-backpack"),
        "text": "Sauce Labs Backpack"
    },
    "tricko": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"),
        "button_remove": (By.ID, "remove-sauce-labs-bolt-t-shirt"),
        "text": "Sauce Labs Bolt T-Shirt"
    },
    "bunda": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-fleece-jacket"),
        "button_remove": (By.ID, "remove-sauce-labs-fleece-jacket"),
        "text": "Sauce Labs Fleece Jacket"
    },
    "svetlo": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-bike-light"),
        "button_remove": (By.ID, "remove-sauce-labs-bike-light"),
        "text": "Sauce Labs Bike Light"
    }
}

#volba dat
def test_items():
    item_1 = "batoh"
    item_2 = "svetlo"
    return item_1, item_2

def test_user_item():
    user_key = "standard"
    user_data = test_users[user_key]
    return user_data["username"], user_data["password"]

#testovaci funkce
def setup():
    options = Options()
    options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerOnboarding,AutofillServerCommunication")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-password-manager-reauthentication")
    options.add_argument("--incognito")
    options.add_argument("--user-data-dir=/tmp/temporary-chrome-profile")

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    driver.get(eshop)
    driver.maximize_window()
    return driver

def login_user(driver, user, password):
    logging.info("START: login user")

    wait_for_element(driver, By.ID, "user-name").send_keys(user)
    wait_for_element(driver, By.ID, "password").send_keys(password)
    wait_for_element(driver, By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    assert "inventory.html" in driver.current_url, "❌ Login failed!"
    print("✅ Login successful!")
    logging.info("okno:inventory")
    logging.info("END: login user")

def open_cart_from_inventory(driver):
    wait_for_element(driver, By.ID, "shopping_cart_container").click()
    WebDriverWait(driver, 10).until(EC.url_contains("cart.html"))
    logging.info("okno:cart")

def return_to_inventory_from_cart(driver):
    wait_for_element(driver, By.ID, "continue-shopping").click()
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    logging.info("okno:inventory")

def add_item_to_cart(driver, goods_item):
    logging.info(f"START: add item to cart for {goods_item}")
    wait_for_element(driver, *goods[goods_item]["button_add"]).click()
    logging.info(f"END: add item to cart for {goods_item}")

def remove_item_from_cart(driver, goods_item):
    logging.info(f"START: remove item from cart for {goods_item}")
    wait_for_element(driver, *goods[goods_item]["button_remove"]).click()
    logging.info(f"END: remove item from cart for {goods_item}")

def cart_contents(driver):
    logging.info("START: vytvoreni seznamu obsahu kosiku")
    v_kosiku = driver.find_elements(By.CLASS_NAME, "cart_item")
    v_kosiku_seznam = []
    for polozka in v_kosiku:
        polozka_nazev = polozka.find_element(By.CLASS_NAME, "inventory_item_name").text
        v_kosiku_seznam.append(polozka_nazev)
    logging.info("END: vytvoreni seznamu obsahu kosiku")
    return v_kosiku_seznam    

def assert_item_in_cart(driver, goods_item):
    logging.info(f"START: test pritomnosti {goods_item} v kosiku")
    v_kosiku_seznam = cart_contents(driver)
    expected_name = goods[goods_item]["text"]
    assert expected_name in v_kosiku_seznam, f"❌ {goods_item} neni kosiku"
    print(f"✅ {goods_item} je v kosiku")
    logging.info(f"END: test pritomnosti {goods_item} v kosiku")

def assert_item_not_in_cart(driver, goods_item):
    logging.info(f"START: test nepritomnosti {goods_item} v kosiku")
    v_kosiku_seznam = cart_contents(driver)
    expected_name = goods[goods_item]["text"]
    assert expected_name not in v_kosiku_seznam, f"❌ {goods_item} je stale v kosiku"
    print(f"✅ {goods_item} neni v kosiku")
    logging.info(f"END: test nepritomnosti {goods_item} v kosiku")
#pomocne funkce
def wait_for_element(driver, by, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, locator))
    )

def teardown(driver):
    #input("Stiskni Enter pro ukončení a zavření prohlížeče...")
    driver.quit()

#test
try:
    driver = setup()
    item_1, item_2 = test_items()
    user, password = test_user_item()
    login_user(driver, user, password)
    goods_item = item_1
    add_item_to_cart(driver, goods_item)
    open_cart_from_inventory(driver)    
    assert_item_in_cart(driver, goods_item)
    return_to_inventory_from_cart(driver)
    goods_item = item_2
    add_item_to_cart(driver, goods_item)
    open_cart_from_inventory(driver)
    assert_item_in_cart(driver, goods_item)
    goods_item = item_1
    remove_item_from_cart(driver, goods_item)
    assert_item_not_in_cart(driver, goods_item)
    goods_item = item_2
    remove_item_from_cart(driver, goods_item)
    assert_item_not_in_cart(driver, goods_item)
    teardown(driver)

except Exception as e:
    print(f"Test Suite selhal s chybou: {e}")
    logging.error(f"Test Suite selhal s chybou: {e}")
