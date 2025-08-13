import os
import time
import logging
from dataclasses import dataclass
from typing import Dict, Tuple, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


BASE_URL = "https://www.saucedemo.com/"

USERS: Dict[str, Dict[str, str]] = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "problem": {"username": "problem_user", "password": "secret_sauce"},
}

LOG_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "run.log"), encoding="utf-8"),
        logging.StreamHandler()
    ],
)
logger = logging.getLogger("SwagLabsTest")


@dataclass
class Waits:
    short: int = 5
    normal: int = 10
    long: int = 20


class BrowserFactory:
    @staticmethod
    def create() -> WebDriver:
        options = Options()
        options.add_argument("--incognito")
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        })
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        logger.info("WebDriver initialized and maximized")
        return driver


class BasePage:
    """Base Page Object"""

    URL: Optional[str] = None

    def __init__(self, driver: WebDriver, waits: Waits = Waits()):
        self.driver = driver
        self.waits = waits
        self.log = logging.getLogger(self.__class__.__name__)

    def open(self) -> "BasePage":
        assert self.URL, "This page has no URL defined."
        self.log.info(f"Opening page: {self.URL}")
        self.driver.get(self.URL)
        return self

    def wait_for(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        t = timeout or self.waits.normal
        self.log.debug(f"Waiting for element {locator} (timeout={t}s)")
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        t = timeout or self.waits.normal
        self.log.debug(f"Waiting for element to be clickable {locator} (timeout={t}s)")
        return WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator: Tuple[str, str]):
        self.log.info(f"Clicking {locator}")
        self.wait_clickable(locator).click()

    def type(self, locator: Tuple[str, str], text: str, clear: bool = True):
        self.log.info(f"Typing into {locator}: '{text}'")
        el = self.wait_for(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def text_of(self, locator: Tuple[str, str]) -> str:
        el = self.wait_for(locator)
        value = el.text
        self.log.debug(f"Text of {locator} = '{value}'")
        return value

    def take_screenshot(self, name_prefix: str = "screenshot") -> str:
        ts = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(LOG_DIR, f"{name_prefix}_{ts}.png")
        self.driver.save_screenshot(path)
        self.log.warning(f"Screenshot saved: {path}")
        return path


class LoginPage(BasePage):
    URL = BASE_URL

    USERNAME = (By.XPATH, "//*[@id='user-name']")
    PASSWORD = (By.XPATH, "//*[@id='password']")
    LOGIN_BTN = (By.XPATH, "//*[@id='login-button']")
    ERROR_MSG = (By.XPATH, "//h3[@data-test='error']")

    def sign_in(self, username: str, password: str) -> "InventoryPage":
        """Signs in a user X"""
        self.log.info(f"Signing in user '{username}'")
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        return InventoryPage(self.driver)

    def sign_in_as(self, user_key: str) -> "InventoryPage":
        creds = USERS[user_key]
        return self.sign_in(creds["username"], creds["password"])

    def should_show_error(self, text_contains: str):
        self.log.info(f"Verifying an error message containing: '{text_contains}'")
        try:
            msg = self.text_of(self.ERROR_MSG)
            assert text_contains in msg, f"Expected error text '{text_contains}', but was '{msg}'"
        except Exception:
            self.take_screenshot("login_error_not_visible")
            raise


class TopMenu(BasePage):
    MENU_BTN = (By.XPATH, "//*[@id='react-burger-menu-btn']")
    LOGOUT_LINK = (By.XPATH, "//*[@id='logout_sidebar_link']")

    def open_menu(self) -> "TopMenu":
        self.log.info("Opening side menu")
        self.click(self.MENU_BTN)
        return self

    def logout(self) -> "LoginPage":
        self.log.info("Logging out")
        self.click(self.LOGOUT_LINK)
        return LoginPage(self.driver)


class InventoryPage(BasePage):
    INVENTORY_CONTAINER = (By.XPATH, "//*[@id='inventory_container']")
    ITEM_TITLES = (By.XPATH, "//*[contains(@class,'inventory_item_name')]")
    FIRST_ADD_TO_CART = (By.XPATH, "(//button[contains(@class,'btn_inventory')])[1]")
    CART_BADGE = (By.XPATH, "//*[contains(@class,'shopping_cart_badge')]")
    BACK_TO_PRODUCTS = (By.XPATH, "//*[@id='back-to-products']")

    def should_be_open(self):
        self.log.info("Verifying that the Inventory page is open")
        try:
            WebDriverWait(self.driver, self.waits.normal).until(
                EC.url_contains("inventory.html")
            )
            self.wait_for(self.INVENTORY_CONTAINER)
        except TimeoutException:
            self.take_screenshot("inventory_not_open")
            raise AssertionError("Inventory page is not open")

    def open_first_product(self) -> "ItemDetailPage":
        self.log.info("Opening the first product in the list")
        item = WebDriverWait(self.driver, self.waits.normal).until(
            EC.visibility_of_any_elements_located(self.ITEM_TITLES)
        )[0]
        name = item.text
        item.click()
        self.log.info(f"Opened product detail: {name}")
        return ItemDetailPage(self.driver, expected_name=name)

    def add_first_listed_item_to_cart(self) -> "InventoryPage":
        self.log.info("Adding the first listed item to the cart")
        self.click(self.FIRST_ADD_TO_CART)
        return self

    def cart_count_should_be(self, expected: int):
        self.log.info(f"Verifying cart item count = {expected}")
        try:
            badge_text = self.text_of(self.CART_BADGE)
            actual = int(badge_text)
            assert actual == expected, f"Expected cart count {expected}, but was {actual}"
        except TimeoutException:
            if expected == 0:
                self.log.info("Cart badge not displayed - expected for 0")
                return
            self.take_screenshot("cart_badge_missing")
            raise AssertionError("Cart badge is missing - possible add-to-cart issue")


class ItemDetailPage(BasePage):
    TITLE = (By.XPATH, "//*[contains(@class,'inventory_details_name')]")
    BACK_BTN = (By.XPATH, "//*[@id='back-to-products']")

    def __init__(self, driver: WebDriver, waits: Waits = Waits(), expected_name: Optional[str] = None):
        super().__init__(driver, waits)
        self.expected_name = expected_name

    def should_be_open(self):
        self.log.info("Verifying that the Item Detail page is open")
        try:
            WebDriverWait(self.driver, self.waits.normal).until(
                EC.url_contains("inventory-item.html")
            )
            self.wait_for(self.TITLE)
        except TimeoutException:
            self.take_screenshot("item_detail_not_open")
            raise AssertionError("Item detail page is not open")

    def should_show_product_name(self):
        if self.expected_name:
            self.log.info(f"Checking product name: '{self.expected_name}'")
            actual = self.text_of(self.TITLE)
            assert self.expected_name == actual, (
                f"Expected name '{self.expected_name}', but was '{actual}'"
            )

    def back_to_products(self) -> "InventoryPage":
        self.log.info("Returning back to product list")
        self.click(self.BACK_BTN)
        return InventoryPage(self.driver)


def _with_screenshot_on_error(page: BasePage, fn, *args, **kwargs):
    """Takes a screenshot if the step fails."""
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        page.take_screenshot(fn.__name__)
        raise e


def test_standard_user_happy_path():
    """
    Scenario: A standard user signs in, opens the first item's detail, goes back, and logs out.
    Expectations: No errors and clear logs.
    """
    driver = BrowserFactory.create()
    try:
        login = LoginPage(driver).open()
        inventory = _with_screenshot_on_error(login, login.sign_in_as, "standard")
        _with_screenshot_on_error(inventory, inventory.should_be_open)

        detail = _with_screenshot_on_error(inventory, inventory.open_first_product)
        _with_screenshot_on_error(detail, detail.should_be_open)
        _with_screenshot_on_error(detail, detail.should_show_product_name)

        inventory = _with_screenshot_on_error(detail, detail.back_to_products)

        menu = TopMenu(driver)
        _with_screenshot_on_error(menu, menu.open_menu)
        login = _with_screenshot_on_error(menu, menu.logout)
        login.open()
    finally:
        driver.quit()


def test_problem_user_add_to_cart_behaviour():
    """
    Scenario: Problem user - test add-to-cart behavior.
    Expectations: After adding the first item, the cart badge should become 1.
    """
    driver = BrowserFactory.create()
    try:
        login = LoginPage(driver).open()
        inventory = login.sign_in_as("problem")
        inventory.should_be_open()

        inventory.add_first_listed_item_to_cart()
        inventory.cart_count_should_be(1)

        menu = TopMenu(driver)
        menu.open_menu().logout()
    finally:
        driver.quit()


def test_negative_login_wrong_password():
    """
    Scenario: Negative login - wrong password.
    Expectations: An error message is displayed.
    """
    driver = BrowserFactory.create()
    try:
        login = LoginPage(driver).open()
        login.sign_in("standard_user", "totally_wrong_password")
        login.should_show_error("Username and password do not match")
    finally:
        driver.quit()


if __name__ == "__main__":
    try:
        logger.info("Running scenario: test_standard_user_happy_path")
        test_standard_user_happy_path()
        logger.info("Running scenario: test_problem_user_add_to_cart_behaviour")
        test_problem_user_add_to_cart_behaviour()
        logger.info("Running scenario: test_negative_login_wrong_password")
        test_negative_login_wrong_password()
    except AssertionError as e:
        logger.error(f"❌ Test failed: {e}")
        raise
    except WebDriverException as e:
        logger.error(f"WebDriver error: {e}")
        raise
    finally:
        logger.info(f"Test run completed. Logs and screenshots are in folder '{LOG_DIR}'.")
