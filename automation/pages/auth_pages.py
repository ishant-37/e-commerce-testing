from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object for the Login Page."""
    
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "btn-login")
    FLASH_MESSAGE = (By.CSS_SELECTOR, ".flash")
    REGISTER_LINK = (By.ID, "link-register")
    EMAIL_ERROR = (By.ID, "email-error")
    PASSWORD_ERROR = (By.ID, "password-error")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:5050/login"

    def navigate(self):
        """Navigate to the login page."""
        self.open_url(self.url)

    def login(self, email, password):
        """Perform login action with provided credentials."""
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_flash_message(self):
        """Return the text of the flash alert message, if present."""
        if self.is_element_visible(self.FLASH_MESSAGE, timeout=3):
            return self.get_text(self.FLASH_MESSAGE)
        return None

    def get_email_error(self):
        if self.is_element_visible(self.EMAIL_ERROR, timeout=2):
             return self.get_text(self.EMAIL_ERROR)
        return ""


class RegisterPage(BasePage):
    """Page Object for the Registration Page."""
    
    # Locators
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirm-password")
    REGISTER_BUTTON = (By.ID, "btn-register")
    FLASH_MESSAGE = (By.CSS_SELECTOR, ".flash")
    LOGIN_LINK = (By.ID, "link-login")
    PASSWORD_ERROR = (By.ID, "password-error")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:5050/register"

    def navigate(self):
        """Navigate to the register page."""
        self.open_url(self.url)

    def register(self, name, email, password, confirm_password):
        """Perform registration action with provided details."""
        self.type_text(self.NAME_INPUT, name)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.type_text(self.CONFIRM_PASSWORD_INPUT, confirm_password)
        self.click(self.REGISTER_BUTTON)

    def get_flash_message(self):
        """Return the text of the flash alert message, if present."""
        if self.is_element_visible(self.FLASH_MESSAGE, timeout=3):
            return self.get_text(self.FLASH_MESSAGE)
        return None
