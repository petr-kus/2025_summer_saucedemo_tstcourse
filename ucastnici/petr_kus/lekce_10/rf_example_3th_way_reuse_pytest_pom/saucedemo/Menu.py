from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Menu:
    main_menu_button = (By.ID, "react-burger-menu-btn")
    logout_button = (By.XPATH,"//nav/*[text()='Logout']")

    def __init__(self, driver):
        self.driver = driver

    def open_menu(self):
        self.driver.find_element(*self.main_menu_button).click()
    
    def press_logout(self):
        WebDriverWait(self.driver,2).until(EC.visibility_of_element_located(self.logout_button)).click()
        
