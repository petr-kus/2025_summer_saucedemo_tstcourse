from pages.base_page import BasePage
from elementy import CheckoutPageLocators

class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, url="https://www.saucedemo.com/checkout-step-one.html")
        self.locators = CheckoutPageLocators

    def enter_checkout_information(self, first_name, last_name, zip_code):
        """Zadá informace o zákazníkovi."""
        first_name_element = self.send_keys_to_element(self.locators.FIRST_NAME_FIELD, first_name, "Jméno")
        if first_name_element:
            self.verify_element_value(first_name_element, first_name, "Jméno")

        last_name_element = self.send_keys_to_element(self.locators.LAST_NAME_FIELD, last_name, "Příjmení")
        if last_name_element:
            self.verify_element_value(last_name_element, last_name, "Příjmení")

        zip_code_element = self.send_keys_to_element(self.locators.ZIP_POSTAL_CODE_FIELD, zip_code, "PSČ")
        if zip_code_element:
            self.verify_element_value(zip_code_element, zip_code, "PSČ")

    def click_continue(self):
        """Klikne na tlačítko 'Continue'."""
        self.click_element(self.locators.CONTINUE_BUTTON, "Tlačítko Pokračovat")

    def click_finish(self):
        """Klikne na tlačítko 'Finish'."""
        self.click_element(self.locators.FINISH_BUTTON, "Tlačítko Dokončit")

    def is_order_complete(self):
        """Ověří, zda je objednávka kompletní."""
        return self.is_element_displayed(self.locators.CHECKOUT_COMPLETE_HEADER, "Potvrzení objednávky")