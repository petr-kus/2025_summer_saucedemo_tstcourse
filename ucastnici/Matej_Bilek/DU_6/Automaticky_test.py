from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def slowdown(seconds=2):
    time.sleep(seconds)

def login(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    slowdown()
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    slowdown()

driver = webdriver.Chrome()
try:
    login(driver, "standard_user", "secret_sauce")
    assert "inventory.html" in driver.current_url, "Not on inventory page"
    print("✅ Login successful!")

    item = driver.find_element(By.CLASS_NAME, "inventory_item_name")
    assert item.is_displayed(), "Item title not visible"
    item_name = item.text
    item.click()
    slowdown()

    assert item_name in driver.page_source, "Product name not on detail page"
    assert "inventory-item.html" in driver.current_url, "Not on item detail page"
    print(f"✅ Product detail page opened for: {item_name}")

    driver.find_element(By.ID, "back-to-products").click()
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    slowdown(1)
    driver.find_element(By.ID, "logout_sidebar_link").click()
    slowdown()
    print("✅ Logout successful!")

    login(driver, "problem_user", "secret_sauce")
    assert "inventory.html" in driver.current_url, "Login failed for problem_user"
    print("✅ Login successful with problem_user!")

finally:
    slowdown()
    driver.quit()
