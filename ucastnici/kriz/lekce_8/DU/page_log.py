from selenium.webdriver.common.by import By

class Page_Logging:    

    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='Username']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Password']")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Login']")    

    def __init__(self, driver, logger, url):
        self.driver = driver
        self.logger = logger
        self.url = url

    def login_user(self, username, password):
        self.logger.info("Otevřena přihlašovací stránka")
        self.driver.get(self.url)
        self.logger.info(f"Pokus o přihlášení uživatele: {username}")
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        self.logger.info("Přihlašovací formulář byl odeslán")

