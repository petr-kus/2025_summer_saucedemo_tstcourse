from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pomocne import wait_for_element

class Page_Logging:    

    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='Username']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Password']")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Login']")    

    def __init__(self, driver, logger, url):
        self.driver = driver
        self.logger = logger
        self.url = url
    
    def login_user(self, username, password):
        self.driver.get(self.url)
        self.logger.info("Otevrena prihlasovaci stranka")
        self.logger.info(f"Pokus o prihlaseni uzivatele: '{username}'")
        wait_for_element(self.driver, *self.USERNAME_INPUT).send_keys(username)
        wait_for_element(self.driver, *self.PASSWORD_INPUT).send_keys(password)
        wait_for_element(self.driver, *self.LOGIN_BUTTON).click()
        self.logger.info("Prihlasovaci formular byl odeslan")
        WebDriverWait(self.driver, 10).until(EC.url_contains("/inventory.html"))
        self.logger.info(f"Prihlaseni jako '{username}' bylo uspesne, jsi na '{self.driver.current_url}'")
        

