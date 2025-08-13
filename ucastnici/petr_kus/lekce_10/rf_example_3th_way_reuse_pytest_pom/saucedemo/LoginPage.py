from selenium.webdriver.common.by import By
from selenium import webdriver

class LoginPage:
    username_field = (By.ID, "user-name")
    password_field = (By.ID, "password")
    submit_button = (By.ID, "login-button")
    page_url = "https://www.saucedemo.com/"

    #not ideal implementation during the lesson
    #def __init__(self):
    #    browser = webdriver.Chrome()
    #    self.driver = browser

    #better implementation
    def open_page(self,url):
        browser = webdriver.Chrome()
        self.driver = browser
        self.driver.get(url)

    def we_are_on_page(self):
        assert self.page_url == self.driver.current_url, f"We are not on the right page '{self.page_url}'"

    def login_user(self, username, password):
        field_username = self.driver.find_element(*self.username_field)
        field_username.send_keys(username)
        field_password = self.driver.find_element(*self.password_field)
        field_password.send_keys(password)
        button_submit = self.driver.find_element(*self.submit_button)
        button_submit.click()

    def is_user_loged(self):
        #TODO: make better verification 
        assert "inventory" in self.driver.current_url, f"Expected 'inventory' in url, but in url '{self.driver.current_url}' was not found."
