from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
from robot.api import logger

class PomocneLibrary:

    def __init__(self):
        self.item_cart = (By.CLASS_NAME, "cart_item")
        self.item_name = (By.CLASS_NAME, "inventory_item_name")

    @property
    def selib(self):
        return BuiltIn().get_library_instance("SeleniumLibrary")

    def cart_contents(self):
        driver = self.selib.driver
        logger.info("START: vytvoreni seznamu obsahu kosiku")
        items = driver.find_elements(*self.item_cart)
        items_in_cart = []
        for item in items:
            name = item.find_element(*self.item_name).text
            items_in_cart.append(name)
        logger.info("END: vytvoreni seznamu obsahu kosiku")
        return items_in_cart