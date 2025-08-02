from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from elementy import LoginPageLocators
import logging

logging.basicConfig(filename="loggy.log",level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")

user = [{"name" : "standard_user", "password" : "secret_sauce"},{"name" : "problem_user", "password" : "secret_sauce"}]

def login_user(driver, user):
    try:
        username = driver.find_element(*LoginPageLocators.USER_NAME_FIELD)
        username.send_keys(user["name"])
        password = driver.find_element(*LoginPageLocators.PASSWORD_FIELD)
        password.send_keys(user["password"])
        login_button = driver.find_element(*LoginPageLocators.LOGIN_BUTTON)
        login_button.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))

        header = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        if header.text == "Products":
            print("Nalezení H1 bylo úspěšné.")
            logging.info("Nalezení H1 bylo úspěšné.")
        else:
            print("H1 neodpovídá")
            logging.warning("H1 neodpovídá")
    except Exception as e:
        print(f"Chyba při přihlašování: '{e}'")
        logging.error(f"Chyba při přihlašování: '{e}'", exc_info=True)


def click(driver, by, selector, popis):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((by, selector)))
        element.click()
        print(f"{popis} OK")
        logging.info(f"{popis} OK")            
        return True
    except:
        print(f"{popis} nefunguje")
        logging.warning(f"{popis} nefunguje")
        return False

def try_send_keys(driver, by, selector, text, popis):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, selector)))
        element.send_keys(text)
        print(f"{popis}'{text}' OK")
        logging.info(f"{popis} '{text}' OK")
        return element
    except:
        print(f"{popis} nefunguje (nelze zadat text)")
        logging.warning(f"{popis} nefunguje (nelze zadat text)")
        return None

def try_get_value(element, expected_value, popis):
    try:
        actual_value = element.get_attribute("value")
        assert actual_value == expected_value
        print(f"{popis} ověřeno OK")
        logging.info(f"{popis} ověřeno OK")
    except Exception as e:
        print(f"{popis} ověření nefunguje (očekáváno '{expected_value}', nalezeno '{actual_value}')")
        logging.warning(f"{popis} ověření nefunguje (očekáváno '{expected_value}', nalezeno '{actual_value}') - {e}")