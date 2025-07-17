from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Funkce pro bezpečné akce ---
def try_click(driver, by, selector, popis):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((by, selector))
        )
        element.click()
        print(f"{popis} OK")
        return True
    except:
        print(f"{popis} nefunguje")
        return False

def try_send_keys(driver, by, selector, text, popis):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, selector))
        )
        element.send_keys(text)
        print(f"{popis} – text '{text}' OK")
        return element
    except:
        print(f"{popis} nefunguje (nelze zadat text)")
        return None

def try_get_value(element, expected_value, popis):
    try:
        actual_value = element.get_attribute("value")
        assert actual_value == expected_value
        print(f"{popis} ověřeno – OK")
    except:
        print(f"{popis} ověření nefunguje (očekáváno '{expected_value}', nalezeno '{actual_value}')")

# --- Nastavení Selenium ---
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)

driver.get("https://www.saucedemo.com/")

# --- Přihlášení ---
username = driver.find_element(By.ID, 'user-name')
username.send_keys('standard_user')  # UŽIVATEL standard_user nebo problem_user
password = driver.find_element(By.ID, 'password')
password.send_keys('secret_sauce')
login_button = driver.find_element(By.ID, 'login-button')
login_button.click()
print("Přihlášení OK")

# --- Přidání do košíku ---
try_click(driver, By.ID, "add-to-cart-sauce-labs-backpack", "Přidání do košíku")

# --- Otevření košíku ---
try_click(driver, By.CLASS_NAME, "shopping_cart_link", "Otevření košíku")

# --- Checkout ---
if try_click(driver, By.ID, "checkout", "Tlačítko Checkout"):

    # --- First Name ---
    first_name = try_send_keys(driver, By.ID, "first-name", "Pavel", "Jméno")
    if first_name:
        try_get_value(first_name, "Pavel", "Jméno")

    # --- Last Name ---
    last_name = try_send_keys(driver, By.ID, "last-name", "Petrle", "Příjmení")
    if last_name:
        try_get_value(last_name, "Petrle", "Příjmení")

# --- Konec ---
time.sleep(6)
driver.quit()
