from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pytest
@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    return driver
@pytest.fixture
def webpage():
    return "https://www.saucedemo.com"
@pytest.fixture
def login():
    return {"username": "standard_user", "password": "secret_sauce"}
class TestWebPage:
    driver = webdriver.Chrome()
    def test_web_loading(self, webpage):
        self.driver.get(webpage)
        assert "Swag Labs" == self.driver.title
    @pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])
    def test_login(self, username, password):
        self.driver.find_element(By.ID, "user-name").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
        assert "Products" == self.driver.title
        self.driver.quit()