#from selenium.webdriver.common.by import By
from pomocne import wait_for_element

class Page_Inventory:

    def __init__(self, driver, logger,name, button_add, button_remove, text):
        self.driver = driver
        self.logger = logger
        self.name = name
        self.button_add = button_add
        self.button_remove = button_remove
        self.text = text

    def add_to_cart(self):
        try:
            self.logger.info(f"Do kosiku pridavam '{self.name}'")
            wait_for_element(self.driver, *self.button_add).click()
        except Exception as e:
            self.logger.error(f"Chyba pri pridavani '{self.name}' do kosiku: {e}")
        raise

    def remove_from_cart(self):
        try:
            self.logger.info(f"Z kosiku odebiram '{self.name}'")
            wait_for_element(self.driver, *self.button_remove).click()
        except Exception as e:
            self.logger.error(f"Chyba pri odebirani '{self.name}' z kosiku: {e}")
        raise



