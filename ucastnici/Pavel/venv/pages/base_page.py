import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException


class BasePage:
    def __init__(self, driver, url=None):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.url = url

    def go_to_page(self):
        if self.url:
            self.driver.get(self.url)
            logging.info(f"Navigace na URL: {self.url}")
        else:
            logging.warning("URL pro tuto stránku není definována v BasePage.")

    def _find_element(self, by_locator, element_name="element"):
        """Nalezne element a čeká na jeho přítomnost."""
        try:
            element = self.wait.until(EC.presence_of_element_located(by_locator))
            logging.debug(f"Element '{element_name}' nalezen: {by_locator}")
            return element
        except TimeoutException:
            logging.error(f"Element '{element_name}' nebyl nalezen v čase: {by_locator}")
            raise NoSuchElementException(f"Element '{element_name}' nebyl nalezen po vypršení času: {by_locator}")
        except Exception as e:
            logging.error(f"Chyba při hledání elementu '{element_name}' {by_locator}: {e}", exc_info=True)
            raise

    def click_element(self, by_locator, element_name="tlačítko"):
        """Klikne na element a čeká na jeho klikatelnost."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(by_locator))
            element.click()
            logging.info(f"Kliknuto na: {element_name} ({by_locator})")
            return True
        except TimeoutException:
            logging.warning(f"{element_name} není klikatelné nebo se nenašlo v čase: {by_locator}")
            return False
        except Exception as e:
            logging.error(f"Chyba při klikání na {element_name} ({by_locator}): {e}", exc_info=True)
            raise

    def send_keys_to_element(self, by_locator, text, element_name="textové pole"):
        """Zadá text do elementu a čeká na jeho přítomnost."""
        try:
            element = self.wait.until(EC.presence_of_element_located(by_locator))
            element.clear()
            element.send_keys(text)
            logging.info(f"Zadán text '{text}' do {element_name} ({by_locator})")
            return element
        except TimeoutException:
            logging.warning(f"{element_name} se nenašlo pro zadání textu: {by_locator}")
            return None
        except Exception as e:
            logging.error(f"Chyba při zadávání textu do {element_name} ({by_locator}): {e}", exc_info=True)
            raise

    def get_element_value(self, element, element_name="pole"):
        """Získá hodnotu atributu 'value' elementu."""
        try:
            value = element.get_attribute("value")
            logging.debug(f"Získána hodnota '{value}' z {element_name}.")
            return value
        except StaleElementReferenceException:
            logging.warning(f"StaleElementReferenceException pro {element_name}. Element již není v DOM.")
            return None
        except Exception as e:
            logging.error(f"Chyba při získávání hodnoty z {element_name}: {e}", exc_info=True)
            raise

    def verify_element_value(self, element, expected_value, element_name="pole"):
        """Ověří hodnotu atributu 'value' elementu."""
        actual_value = self.get_element_value(element, element_name)
        if actual_value is not None:
            if actual_value == expected_value:
                logging.info(f"{element_name} ověřeno OK. Očekáváno/Nalezeno: '{expected_value}'")
                print(f"{element_name} ověřeno OK")
                return True
            else:
                logging.warning(f"{element_name} ověření NEFUNGUJE. Očekáváno '{expected_value}', Nalezeno '{actual_value}'")
                print(f"{element_name} ověření NEFUNGUJE")
                return False
        return False 

    def wait_for_url_contains(self, partial_url):
        """Čeká, dokud URL neobsahuje zadaný řetězec."""
        try:
            self.wait.until(EC.url_contains(partial_url))
            logging.info(f"URL obsahuje '{partial_url}' - úspěšně.")
            return True
        except TimeoutException:
            logging.warning(f"URL neobsahuje '{partial_url}' v daném čase. Aktuální URL: {self.driver.current_url}")
            return False
        except Exception as e:
            logging.error(f"Chyba při čekání na URL: {e}", exc_info=True)
            raise

    def get_element_text(self, by_locator, element_name="element"):
        """Získá text z elementu."""
        try:
            element = self.wait.until(EC.presence_of_element_located(by_locator))
            text = element.text
            logging.debug(f"Získán text '{text}' z {element_name} ({by_locator})")
            return text
        except TimeoutException:
            logging.warning(f"Element '{element_name}' nebyl nalezen pro získání textu: {by_locator}")
            return None
        except Exception as e:
            logging.error(f"Chyba při získávání textu z {element_name} ({by_locator}): {e}", exc_info=True)
            raise

    def is_element_displayed(self, by_locator, element_name="element"):
        """Zkontroluje, zda je element viditelný."""
        try:
            element = self.wait.until(EC.visibility_of_element_located(by_locator))
            return element.is_displayed()
        except TimeoutException:
            logging.debug(f"Element '{element_name}' není viditelný: {by_locator}")
            return False
        except Exception as e:
            logging.error(f"Chyba při kontrole viditelnosti elementu '{element_name}' {by_locator}: {e}", exc_info=True)
            return False