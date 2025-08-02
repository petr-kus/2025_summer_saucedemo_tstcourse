from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import logging

logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

import time

test_page = "https://www.saucedemo.com/"
username = "standard_user"
password = "seacrate_sauce"

def log_test_false_for_me(e):
        print(f"Test xyz faild with error {e}")
        logging.error(f'This is an info message. {e}')
        
def setup(test_page):
    driver = webdriver.Chrome()
    driver.get(test_page)
    return driver

def test_login_user(username,password):
    try:
        logging.info(f'login test user {username} {password}')
        field_username = driver.find_element(By.ID, "user-name")
        field_username.send_keys(username)
        field_password = driver.find_element(By.ID, "password")
        field_password.send_keys(password)
        button_submit = driver.find_element(By.ID, "login-button")
        button_submit.click()
        logging.info(f'Test with {username} {password} passed')
    except Exception as e:
        log_test_false_for_me(e)

def teardown():
    driver.quit()

#TEST EXECUTION
driver = setup(test_page)
test_login_user(username,password)
teardown()