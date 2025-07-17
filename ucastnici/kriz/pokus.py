from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Spusť prohlížeč
driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com/")

# Přihlašovací údaje (demo přístup)
username = driver.find_element(By.ID, "user-name")
password = driver.find_element(By.ID, "password")

username.send_keys("standard_user")
password.send_keys("secret_sauce")

driver.find_element(By.ID, "login-button").click()
time.sleep(5)

# Přidej nějaké zboží do košíku
driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()

# Přejdi do košíku
driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

# Počkej, než se stránka načte
time.sleep(1)

# Získej seznam všech položek v košíku
items = driver.find_elements(By.CLASS_NAME, "cart_item")

# Projdi položky a vytiskni název + počet kusů
for item in items:
    name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
    qty = item.find_element(By.CLASS_NAME, "cart_quantity").text
    #print(name)
    print(f"{name} — {qty} ks")

# Zavři prohlížeč
driver.quit()