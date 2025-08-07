from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class LoginPage:
    
    USER_NAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    
    def __init__(self, driver):
        self.driver = driver
        
    def go_to_page(self):
        self.driver.get("https://www.saucedemo.com/")
        logging.info("Navigace na přihlašovací stránku.")

    def login(self, username, password):
        logging.info(f"Pokus o přihlášení uživatele: {username}")
        self.driver.find_element(*self.USER_NAME_FIELD).send_keys(username)
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def is_login_successful(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.url_contains("/inventory.html"))
            return True
        except:
            logging.warning("Přihlášení selhalo, URL neobsahuje '/inventory.html'.")
            return False