from selenium.webdriver.common.by import By
import logging

class CheckoutPage:
    
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")  
    ZIP_POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    CHECKOUT_COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    
    def __init__(self, driver):
        self.driver = driver
    
    def enter_checkout_information(self, first_name, last_name, postal_code):
        self.driver.find_element(*self.FIRST_NAME_FIELD).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_FIELD).send_keys(last_name)
        self.driver.find_element(*self.ZIP_POSTAL_CODE_FIELD).send_keys(postal_code)
        logging.info("Checkout information entered.")

    def click_continue(self):
        self.driver.find_element(*self.CONTINUE_BUTTON).click()
        logging.info("Clicked continue button.")

    def click_finish(self):
        self.driver.find_element(*self.FINISH_BUTTON).click()
        logging.info("Clicked finish button.")

    def is_checkout_complete(self):
        try:
            return self.driver.find_element(*self.CHECKOUT_COMPLETE_HEADER).text == "Thank you for your order!"
        except:
            return False