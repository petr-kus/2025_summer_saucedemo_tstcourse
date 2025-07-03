from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com/")

#time.sleep(1)  # Wait for page to load

# Find username and password fields and login button
field_username = driver.find_element(By.ID, "user-name")
field_username.send_keys("standard_user")

field_password = driver.find_element(By.ID, "password")
field_password.send_keys("secret_sauce")

button_submit = driver.find_element(By.ID, "login-button")
button_submit.click()

time.sleep(5)  # Wait to see result

driver.quit()