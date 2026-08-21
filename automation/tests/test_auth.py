import time
from automation.pages.auth_pages import LoginPage, RegisterPage
from app.database import get_db_connection

def test_successful_registration(driver):
    """Test that a new user can successfully register an account."""
    # We generate a unique email using timestamp to avoid duplicate errors on subsequent test runs
    unique_email = f"testuser_{int(time.time())}@example.com"
    
    register_page = RegisterPage(driver)
    register_page.navigate()
    
    register_page.register("Test User", unique_email, "SecurePass123", "SecurePass123")
    
    # Wait for the success flash message and redirection
    flash_msg = register_page.get_flash_message()
    assert "Registration successful" in flash_msg, f"Expected success message, got: {flash_msg}"
    
    # Optional: Verify in DB directly to ensure data integrity
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (unique_email,))
    user = cursor.fetchone()
    conn.close()
    assert user is not None, "User was not found in the database after registration"


def test_invalid_login_credentials(driver):
    """Test that login fails with incorrect credentials."""
    login_page = LoginPage(driver)
    login_page.navigate()
    
    login_page.login("wrong@email.com", "wrongpassword")
    
    flash_msg = login_page.get_flash_message()
    assert "Invalid email or password" in flash_msg, f"Expected invalid credentials error, got: {flash_msg}"


def test_successful_login(driver):
    """Test that an existing user can log in successfully."""
    # First, ensure a user exists. We'll use the unique email strategy again just in case,
    # but we have to register them first within this test setup.
    unique_email = f"loginuser_{int(time.time())}@example.com"
    password = "MyPassword123"
    
    # Setup: Register the user
    register_page = RegisterPage(driver)
    register_page.navigate()
    register_page.register("Login User", unique_email, password, password)
    time.sleep(2) # Give it a moment to redirect to login page
    
    # Test: Login with the newly created user
    login_page = LoginPage(driver)
    # The registration redirects to login, but we explicitly navigate to be safe
    login_page.navigate() 
    
    login_page.login(unique_email, password)
    
    flash_msg = login_page.get_flash_message()
    assert "Login successful" in flash_msg, f"Expected login success message, got: {flash_msg}"
    
    # Verify we are redirected to the products page after login
    time.sleep(1.5) # Wait for JS redirect
    assert "/products" in driver.current_url, "User was not redirected to products page after login"
