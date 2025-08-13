"""shop = "https://www.saucedemo.com/"

test_users = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "locked_out": {"username": "locked_out_user", "password": "secret_sauce"},
    "problem": {"username": "problem_user", "password": "secret_sauce"},
    "performance_glitch": {"username": "performance_glitch_user", "password": "secret_sauce"},
    "error": {"username": "error_user", "password": "secret_sauce"},
    "visual": {"username": "visual_user", "password": "secret_sauce"}
}

goods = {
    "batoh": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-backpack"),
        "button_remove": (By.ID, "remove-sauce-labs-backpack"),
        "text": "Sauce Labs Backpack"
    },
    "tricko": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"),
        "button_remove": (By.ID, "remove-sauce-labs-bolt-t-shirt"),
        "text": "Sauce Labs Bolt T-Shirt"
    },
    "bunda": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-fleece-jacket"),
        "button_remove": (By.ID, "remove-sauce-labs-fleece-jacket"),
        "text": "Sauce Labs Fleece Jacket"
    },
    "svetlo": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-bike-light"),
        "button_remove": (By.ID, "remove-sauce-labs-bike-light"),
        "text": "Sauce Labs Bike Light"
    }
}
"""

#########################################################################################
from selenium.webdriver.common.by import By

shop = "https://www.saucedemo.com/"

class Goods:
    def __init__(self, driver):
        self.items =  {
    "batoh": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-backpack"),
        "button_remove": (By.ID, "remove-sauce-labs-backpack"),
        "text": "Sauce Labs Backpack"
    },
    "tricko": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"),
        "button_remove": (By.ID, "remove-sauce-labs-bolt-t-shirt"),
        "text": "Sauce Labs Bolt T-Shirt"
    },
    "bunda": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-fleece-jacket"),
        "button_remove": (By.ID, "remove-sauce-labs-fleece-jacket"),
        "text": "Sauce Labs Fleece Jacket"
    },
    "svetlo": {
        "button_add": (By.ID, "add-to-cart-sauce-labs-bike-light"),
        "button_remove": (By.ID, "remove-sauce-labs-bike-light"),
        "text": "Sauce Labs Bike Light"
    },
    }

    def get(self, name):
        return self.items.get(name)

    def all(self):
        return self.items.values()