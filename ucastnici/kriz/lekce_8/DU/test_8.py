from selenium import webdriver
from page_log import Page_Logging
import logging



driver = webdriver.Chrome()
logging.basicConfig(
    filename='my_log.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s [%(name)s]: %(message)s'
)
logger = logging.getLogger()
url = "https://www.saucedemo.com/"
logger.info("aha")

def teardown(driver):
    input("Stiskni Enter pro ukončení a zavření prohlížeče...")
    driver.quit()

page = Page_Logging(driver, logger, url)
page.login_user("standard_user", "secret_sauce")

teardown(driver)