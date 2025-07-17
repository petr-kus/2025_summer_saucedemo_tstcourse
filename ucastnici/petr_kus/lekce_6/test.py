from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def slowdown():
        time.sleep(3)

# Set up the Chrome WebDriver
driver = webdriver.Chrome()


try:
    # Open the website
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()

    slowdown()

    # Find username and password input fields and login button
    username_input = driver.find_element(By.ID, "user-name")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    # Fill in the login form
    username_input.send_keys("standard_user")
    slowdown()
    password_input.send_keys("secret_sauce")
    slowdown()

    # Click the login button
    login_button.click()

    slowdown()

    # Check if we’re on the inventory page
    if "inventory.html" in driver.current_url:
        print("✅ Login successful!")
    else:
        print("❌ Login failed!")

finally:
    # Close the browser after a short delay
    slowdown()
    driver.quit()