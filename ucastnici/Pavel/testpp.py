from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from modul_testpp import click, try_get_value, try_send_keys, login_user
from elementy import InventoryPageLocators, CartPageLocators, CheckoutPageLocators
import time
import logging

eshop = "https://www.saucedemo.com/"
user = [{"name" : "standard_user", "password" : "secret_sauce"},{"name" : "problem_user", "password" : "secret_sauce"}]


logging.basicConfig(filename="loggy.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)

try: 
    driver.get(eshop)
    login_user(driver, user[0])  
    login_user(driver, user[1])
    
    click(driver, *InventoryPageLocators.ADD_TO_CART_BACKPACK_BUTTON, "Přidání do košíku")
    click(driver, *CartPageLocators.SHOPPING_CART_LINK, "Otevření košíku")

    if click(driver, *CartPageLocators.CHECKOUT_BUTTON, "Tlačítko Checkout"):
    
        first_name = try_send_keys(driver, *CheckoutPageLocators.FIRST_NAME_FIELD, "Pavel", "Jméno")
        if first_name:
           try_get_value(first_name, "Pavel", "Jméno")
           
    last_name = try_send_keys(driver, *CheckoutPageLocators.LAST_NAME_FIELD, "Petrle", "Příjmení")
    if last_name:
        try_get_value(last_name, "Petrle", "Příjmení")
        click(driver, *CheckoutPageLocators.CONTINUE_BUTTON, "Tlačítko Pokračovat")

except Exception as e:
   print(f"Test selhal: {e}")
   logging.error(f"Test selhal: {e}", exc_info=True)
finally:
   time.sleep(6)
   driver.quit()
   logging.info("Prohlížeč byl zavřen.")
