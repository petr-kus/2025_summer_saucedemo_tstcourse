from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging 

#configuration 
logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

#paramters of test 
eshop = "https://www.saucedemo.com/"
user = { "name": "standard_user", 
         "password": "secret_sauce"
       }

#ui elements adresses
button_backpack_add_to_cart = (By.ID,"add-to-cart-sauce-labs-backpack")

def slowdown():
        time.sleep(1)

def setup():
     driver = webdriver.Chrome()
     driver.get(eshop)
     driver.maximize_window()
     return driver

def login_user(user):
     logging.info("START: Test Case login user")
     driver.find_element(By.ID, "user-name").send_keys(user['name'])
     driver.find_element(By.ID, "password").send_keys(user['password'])
     driver.find_element(By.ID, "login-button").click()
     assert "inventory.html" in driver.current_url, "❌ Login failed!"
     print("✅ Login successful!")
     logging.info("END: Test Case login user")

def add_item_to_basket():
     logging.info("START: Test Case add_item_to_basket")
     batoh_do_kosiku = driver.find_element(*button_backpack_add_to_cart)
     do_kosiku = driver.find_element(By.ID, "shopping_cart_container")

     #prvni nakup
     batoh_do_kosiku.click()
     slowdown()
     do_kosiku.click()
     logging.info("END: Test Case login user")

def teardown():
     driver.quit()
    
#TEST EXECUTION
try:
    
    driver = setup()
    login_user(user)
    basket_items = add_item_to_basket()
    basket_items = add_item_to_basket(basket_items)
    teardown()

except Exception as e: 
    logging.error("Test Suite selhal s chybou '{e}'")
    
    