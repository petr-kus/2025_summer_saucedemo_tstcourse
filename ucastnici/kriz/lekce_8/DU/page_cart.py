from selenium.webdriver.common.by import By

class Page_Cart:

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        
    def cart_contents(self, driver):
        self.logger.info("START: vytvoreni seznamu obsahu kosiku")
        v_kosiku = driver.find_elements(By.CLASS_NAME, "cart_item")
        v_kosiku_seznam = []
        for polozka in v_kosiku:
            polozka_nazev = polozka.find_element(By.CLASS_NAME, "inventory_item_name").text
            v_kosiku_seznam.append(polozka_nazev)
        self.logger.info("END: vytvoreni seznamu obsahu kosiku")
        return v_kosiku_seznam    

    def assert_item_in_cart(self, driver, goods_item):
        self.logger.info(f"START: test pritomnosti {goods_item} v kosiku")
        v_kosiku_seznam = cart_contents(driver)
        expected_name = goods[goods_item]["text"]
        assert expected_name in v_kosiku_seznam, f"❌ {goods_item} neni kosiku"
        print(f"✅ {goods_item} je v kosiku")
        self.logger.info(f"END: test pritomnosti {goods_item} v kosiku")

    def assert_item_not_in_cart(self, driver, goods_item):
        self.logger.info(f"START: test nepritomnosti {goods_item} v kosiku")
        v_kosiku_seznam = cart_contents(driver)
        expected_name = goods[goods_item]["text"]
        assert expected_name not in v_kosiku_seznam, f"❌ {goods_item} je stale v kosiku"
        print(f"✅ {goods_item} neni v kosiku")
        self.logger.info(f"END: test nepritomnosti {goods_item} v kosiku")