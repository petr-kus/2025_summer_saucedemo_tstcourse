from selenium.webdriver.common.by import By

import logging

logging.basicConfig(filename="loggy.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class login:
    USER_NAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    DRIVER = "driver"
    
    def __init__(self, driver):
        self.DRIVER = driver
    
    def login_user(self, user):
      username = self.DRIVER.find_element(*self.USER_NAME_FIELD)
      username.send_keys(user["name"])
      password = self.DRIVER.find_element(*self.PASSWORD_FIELD)
      password.send_keys(user["password"])
      login_button = self.DRIVER.find_element(*self.LOGIN_BUTTON)
      login_button.click()