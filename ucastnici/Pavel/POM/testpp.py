from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
#from logging_config import login
import os
import time
import logging

log_path = os.path.abspath("loggy.log")   
logging.basicConfig(filename="loggy.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

eshop_url = "https://www.saucedemo.com/"
# Uživatelé by ideálně měli být načteni z konfiguračního souboru nebo databáze
user = [{"name": "standard_user", "password": "secret_sauce"},
     {"name": "problem_user", "password": "secret_sauce"}]

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)

try:
    logging.info("Spouštění testu nákupu produktu.")

    #driver.get(eshop_url)
    #login_page = login(driver)
    #login_page.login_user(user[1])

    driver.get(eshop_url)
    login_page = LoginPage(driver)
    login_page.go_to_page()
    login_page.login(user[0]["name"], user[0]["password"])

    if not login_page.is_login_successful():
        raise Exception("Nepodařilo se přihlásit uživatele standard_user.")

    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart("Sauce Labs Backpack")

    cart_page = inventory_page.open_cart()
   
    if not cart_page.is_item_in_cart("Sauce Labs Backpack"):
        raise Exception("Položka 'Sauce Labs Backpack' nebyla nalezena v košíku.")

    checkout_page = cart_page.click_checkout()
    if not checkout_page:
        raise Exception("Nepodařilo se přejít na stránku pokladny.")

    checkout_page.enter_checkout_information("Pavel", "Petrle", "12345")
    checkout_page.click_continue()

    logging.info("Test nákupu produktu byl úspěšný.")
    print("Test nákupu produktu byl úspěšný.")

except Exception as e:
    print(f"Test selhal: {e}")
    logging.error(f"Test selhal: {e}", exc_info=True)
finally:
    time.sleep(3)
    driver.quit()
    logging.info("Prohlížeč byl zavřen.")