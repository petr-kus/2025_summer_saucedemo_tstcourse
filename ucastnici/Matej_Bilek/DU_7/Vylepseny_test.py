from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"
USERS = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "problem": {"username": "problem_user", "password": "secret_sauce"}
}

ELEMENTS = {
    "username": (By.ID, "user-name"),
    "password": (By.ID, "password"),
    "login_btn": (By.ID, "login-button"),
    "item_title": (By.CLASS_NAME, "inventory_item_name"),
    "back_btn": (By.ID, "back-to-products"),
    "menu_btn": (By.ID, "react-burger-menu-btn"),
    "logout_link": (By.ID, "logout_sidebar_link")
}


# zruseni chrome popupu
def create_driver():
    options = Options()
    options.add_argument("--incognito")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })
    return webdriver.Chrome(options=options)

def find(driver, key):
    by, value = ELEMENTS[key]
    return driver.find_element(by, value)

def login(driver, user):
    try:
        driver.get(BASE_URL)
        driver.maximize_window()
        find(driver, "username").send_keys(user["username"])
        find(driver, "password").send_keys(user["password"])
        find(driver, "login_btn").click()
    except Exception as e:
        raise Exception(f"Login error: {e}")

def logout(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(ELEMENTS["menu_btn"])
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(ELEMENTS["logout_link"])
        ).click()
    except Exception as e:
        raise Exception(f"Logout error: {e}")

def assert_logged_in(driver):
    if "inventory.html" not in driver.current_url:
        raise AssertionError("❌ Login redirection failed")

def open_first_product(driver):
    try:
        item = find(driver, "item_title")
        assert item.is_displayed(), "Product title not found"
        name = item.text
        item.click()
        assert name in driver.page_source, "Product name not found on details page"
        assert "inventory-item.html" in driver.current_url, "Not on item details page"
        return name
    except Exception as e:
        raise Exception(f"Opening product error: {e}")


def test_standard_user_flow(driver):
    print("Testing standard_user:")
    try:
        login(driver, USERS["standard"])
        assert_logged_in(driver)
        print("✅ Login successful")
        product = open_first_product(driver)
        print(f"✅ Opened product: {product}")
        find(driver, "back_btn").click()
        logout(driver)
        print("✅ Logout successful") 
    except Exception as e:
        print(f"❌ Test failed for standard_user: {e}")

def test_problem_user_login(driver):
    print("Testing problem_user:")
    login(driver, USERS["problem"])
    try:
        assert_logged_in(driver)
        print("✅ Login successful")
    except AssertionError:
        print("❌ Login failed")
    logout(driver)
    print("✅ Logout successful") 


if __name__ == "__main__":
    driver = create_driver()
    try:
        test_standard_user_flow(driver)
        test_problem_user_login(driver)
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
    finally:
        driver.quit()

