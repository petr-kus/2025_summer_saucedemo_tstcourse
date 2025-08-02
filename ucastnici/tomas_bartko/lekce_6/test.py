from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


def slowdown():
    """Helper function for delays"""
    time.sleep(2)


def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)


def test_standard_user_shopping():
    """Test standard user can login and shop"""
    driver = setup_driver()
    
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

        # Check if we're on the inventory page
        assert "inventory.html" in driver.current_url, "Login failed - not on inventory page"
        print("✅ Login successful for standard_user!")

        # Find all "Add to cart" buttons
        add_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class*='btn_inventory']")
        print(f"Found {len(add_buttons)} products")

        # Add first 3 products to cart
        products_added = 0
        for i, button in enumerate(add_buttons[:3]):
            if button.text == "Add to cart":
                # Find product name in the same inventory item
                inventory_item = button.find_element(By.XPATH, "../../..")
                product_name = inventory_item.find_element(By.CLASS_NAME, "inventory_item_name").text
                print(f"Adding product: {product_name}")
                button.click()
                slowdown()
                products_added += 1

        print(f"✅ Added {products_added} products to cart")

        # Check cart badge
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        cart_count = int(cart_badge.text)
        assert cart_count == products_added, f"Cart shows {cart_count}, expected {products_added}"
        print(f"✅ Cart badge shows correct count: {cart_count}")

        # Go to cart
        cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        slowdown()

        # Verify cart page
        assert "cart.html" in driver.current_url, "Not on cart page"
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == products_added, f"Cart page shows {len(cart_items)} items, expected {products_added}"
        print(f"✅ Cart page shows {len(cart_items)} items correctly")

        # Test checkout button exists
        checkout_button = driver.find_element(By.ID, "checkout")
        assert checkout_button.is_displayed(), "Checkout button not visible"
        print("✅ Checkout button is available")

    finally:
        slowdown()
        driver.quit()


def test_problem_user_issues():
    """Test problem_user to demonstrate known issues"""
    driver = setup_driver()
    
    try:
        # Login as problem_user
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()
        slowdown()

        username_input = driver.find_element(By.ID, "user-name")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        username_input.send_keys("problem_user")
        password_input.send_keys("secret_sauce")
        login_button.click()
        slowdown()

        assert "inventory.html" in driver.current_url, "Login failed for problem_user"
        print("✅ Login successful for problem_user!")

        # Try to add products (this user has issues)
        add_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class*='btn_inventory']")
        initial_cart_count = 0
        
        # Get initial cart count
        cart_badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        if cart_badges:
            initial_cart_count = int(cart_badges[0].text)

        print(f"Initial cart count: {initial_cart_count}")

        # Try to add first product
        first_button = add_buttons[0]
        inventory_item = first_button.find_element(By.XPATH, "../../..")
        product_name = inventory_item.find_element(By.CLASS_NAME, "inventory_item_name").text
        print(f"Trying to add: {product_name}")
        first_button.click()
        slowdown()

        # Check if product was actually added
        cart_badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        final_cart_count = int(cart_badges[0].text) if cart_badges else 0
        
        if final_cart_count > initial_cart_count:
            print(f"✅ Product added successfully (cart: {final_cart_count})")
        else:
            print(f"❌ Product NOT added - problem_user bug detected! (cart: {final_cart_count})")

    finally:
        slowdown()
        driver.quit()


def test_invalid_user():
    """Test login with invalid credentials"""
    driver = setup_driver()
    
    try:
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()
        slowdown()

        username_input = driver.find_element(By.ID, "user-name")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        # Try invalid credentials
        username_input.send_keys("invalid_user")
        password_input.send_keys("wrong_password")
        login_button.click()
        slowdown()

        # Should stay on login page
        assert "inventory.html" not in driver.current_url, "Invalid login should not succeed"
        
        # Check for error message
        error_message = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error_message.is_displayed(), "Error message should be visible"
        print(f"✅ Invalid login properly rejected with error: {error_message.text}")

    finally:
        slowdown()
        driver.quit()


if __name__ == "__main__":
    print("🚀 Starting SauceDemo Test Suite...")
    print("\n" + "="*50)
    
    print("\n1. Testing standard_user shopping flow...")
    test_standard_user_shopping()
    
    print("\n2. Testing problem_user issues...")
    test_problem_user_issues()
    
    print("\n3. Testing invalid login...")
    test_invalid_user()
    
    print("\n" + "="*50)
    print("🎉 All tests completed!")