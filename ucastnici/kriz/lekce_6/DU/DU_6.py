from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def slowdown():
        time.sleep(1)

#def kontrola_kosiku():
def seznam_v_kosiku():
    v_kosiku = driver.find_elements(By.CLASS_NAME, "cart_item")

    v_kosiku_seznam = []
    for polozka in v_kosiku:
        polozka_nazev = polozka.find_element(By.CLASS_NAME, "inventory_item_name").text
        v_kosiku_seznam.append(polozka_nazev)
    return v_kosiku_seznam
     
     

# Set up the Chrome WebDriver
driver = webdriver.Chrome()


try:
    # Open the website
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()

    slowdown()

    # Find username and password input fields and login button
    username_input = driver.find_element(By.ID, "user-name")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    
    # Fill in the login form
    username_input.send_keys("standard_user")
    slowdown()
    password_input.send_keys("secret_sauce")
    slowdown()

    # Click the login button
    login_button.click()

    slowdown()
    # Stránka https://www.saucedemo.com/inventory.html
    # Check if we’re on the inventory page
    assert "inventory.html" in driver.current_url, "❌ Login failed!"
    print("✅ Login successful!")
   

    slowdown()
    batoh_do_kosiku = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    do_kosiku = driver.find_element(By.ID, "shopping_cart_container")

    #prvni nakup
    batoh_do_kosiku.click()
    slowdown()
    do_kosiku.click()
    slowdown()

    # Stránka https://www.saucedemo.com/cart.html
    zpet_k_nakupu = driver.find_element(By.ID, "continue-shopping")
     
    v_kosiku_seznam = seznam_v_kosiku()
      
    #je v košíku správné zboží?
    assert "Sauce Labs Backpack" in v_kosiku_seznam, "❌ batoh nepridan"
    print("✅ batoh pridan")
    
    zpet_k_nakupu.click()

    # Stránka https://www.saucedemo.com/inventory.html
    #druhy_nakup

    svetlo_do_kosiku = driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light")
    do_kosiku = driver.find_element(By.ID, "shopping_cart_container")
    
    svetlo_do_kosiku.click()
    slowdown()
    do_kosiku.click()
    slowdown()

    # Stránka https://www.saucedemo.com/cart.html
   
    v_kosiku_seznam = seznam_v_kosiku()

    #je v košíku správné zboží?
    assert "Sauce Labs Bike Light" in v_kosiku_seznam, "❌ svetlo nepridano"
    print("✅ svetlo pridano")
    
    
    #odebrání batohu z košíku

    batoh_z_kosiku = driver.find_element(By.ID, "remove-sauce-labs-backpack")
    batoh_z_kosiku.click()
    v_kosiku_seznam = seznam_v_kosiku()

    assert "Sauce Labs Backpack" not in v_kosiku_seznam, "❌ batoh neodebrán"
    print("✅ batoh odebrán")
    
     #odebrání světla z košíku

    svetlo_z_kosiku = driver.find_element(By.ID, "remove-sauce-labs-bike-light")
    svetlo_z_kosiku.click()
    v_kosiku_seznam = seznam_v_kosiku()

    assert "Sauce Labs Bike Light" not in v_kosiku_seznam, "❌ svetlo neodebráno"
    print("✅ svetlo odebráno")
  

finally:
    # Close the browser after a short delay
    slowdown()
    #input("Test skončil. Stiskni Enter pro zavření prohlížeče...")
    
    driver.quit()