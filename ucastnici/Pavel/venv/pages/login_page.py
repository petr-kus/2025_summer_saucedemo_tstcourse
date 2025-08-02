    
from pages.base_page import BasePage
from elementy import LoginPageLocators, InventoryPageLocators
from selenium.webdriver.common.by import By
import logging


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, url="https://www.saucedemo.com/")
        self.locators = LoginPageLocators
        self.inventory_locators = InventoryPageLocators

    def login(self, username, password):
        logging.info(f"Pokus o přihlášení uživatele: {username}")
        self.send_keys_to_element(self.locators.USER_NAME_FIELD, username, "Uživatelské jméno")
        self.send_keys_to_element(self.locators.PASSWORD_FIELD, password, "Heslo")
        self.click_element(self.locators.LOGIN_BUTTON, "Tlačítko Přihlásit")

    def is_login_successful(self):
        if self.wait_for_url_contains("/inventory.html"):
            header_text = self.get_element_text(self.inventory_locators.PRODUCTS_HEADER, "Nadpis Stránky Produktů")
            if header_text == "Products":
                logging.info("Nalezení H1 'Products' bylo úspěšné. Přihlášení proběhlo OK.")
                print("Nalezení H1 'Products' bylo úspěšné. Přihlášení proběhlo OK.")
                return True
            else:
                logging.warning(f"H1 neodpovídá 'Products'. Nalezeno: '{header_text}'")
                print(f"H1 neodpovídá 'Products'. Nalezeno: '{header_text}'")
                return False
        else:
            logging.warning("Přihlášení selhalo, URL neobsahuje '/inventory.html'.")
            return False

    def get_error_message(self):
        error_locator = (By.XPATH, "//h3[@data-test='error']")
        return self.get_element_text(error_locator, "Chybová zpráva")