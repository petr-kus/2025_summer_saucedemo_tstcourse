from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pomocne import wait_for_element

class Page_Cart:
    item_cart = (By.CLASS_NAME, "cart_item")
    item_name = (By.CLASS_NAME, "inventory_item_name")
    cart_button = (By.ID, "shopping_cart_container")
    continue_shopping_button = (By.ID, "continue-shopping")

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def open_cart_from_inventory(self):
        wait_for_element(self.driver, *self.cart_button).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("cart.html"))
        self.logger.info("okno:cart")

    def cart_contents(self):
        self.logger.info("START: vytvoreni seznamu obsahu kosiku")
        v_kosiku = self.driver.find_elements(*self.item_cart)
        v_kosiku_seznam = []
        for polozka in v_kosiku:
            polozka_nazev = polozka.find_element(*self.item_name).text
            v_kosiku_seznam.append(polozka_nazev)
        self.logger.info("END: vytvoreni seznamu obsahu kosiku")
        return v_kosiku_seznam    

    def assert_item_in_cart(self, text):
        self.logger.info(f"START: test pritomnosti '{text}' v kosiku")
        v_kosiku_seznam = self.cart_contents()
        assert text in v_kosiku_seznam, f"Polozka '{text}' neni v kosiku"
        self.logger.info(f"'{text}' je v kosiku")
        self.logger.info(f"END: test pritomnosti '{text}' v kosiku")

    def assert_item_not_in_cart(self, text):
        self.logger.info(f"START: test nepritomnosti '{text}' v kosiku")
        v_kosiku_seznam = self.cart_contents()
        assert text not in v_kosiku_seznam, f"Polozka '{text}' je stale v kosiku"
        self.logger.info(f"'{text}' neni v kosiku")
        self.logger.info(f"END: test nepritomnosti '{text}' v kosiku")

    def return_to_inventory_from_cart(self):
        wait_for_element(self.driver, *self.continue_shopping_button).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("inventory.html"))
        self.logger.info("okno:inventory")
