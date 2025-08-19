from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

logger = logging.getLogger(__name__)

class CheckoutPage:
    
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")  
    ZIP_POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    CHECKOUT_COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    
    def __init__(self, driver):
        self.driver = driver
        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
      
      
    
    def enter_checkout_information(self, first_name, last_name, postal_code):
        self.driver.find_element(*self.FIRST_NAME_FIELD).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_FIELD).send_keys(last_name)
        self.driver.find_element(*self.ZIP_POSTAL_CODE_FIELD).send_keys(postal_code)
        logger.info("Checkout - informace vložené.")

    def click_continue(self):
        self.driver.find_element(*self.CONTINUE_BUTTON).click()
        logger.info("Kliknuto na tlačítko pokračovat.")

    def click_finish(self):
        self.driver.find_element(*self.FINISH_BUTTON).click()
        logger.info("Kliknuto na ukončovací tlačítko.")

    def is_checkout_complete(self):
        try:
            return self.driver.find_element(*self.CHECKOUT_COMPLETE_HEADER).text == "Thank you for your order!"
        except:
          
            logger.warning("Checkout completion header not found or text mismatch.")
        return False