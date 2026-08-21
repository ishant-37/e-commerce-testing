from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    Base class for all Page Objects.
    Contains common methods for interacting with web elements using explicit waits.
    """
    def __init__(self, driver):
        self.driver = driver
        # Default explicit wait time for elements to appear/become interactable
        self.wait = WebDriverWait(self.driver, 10) 

    def open_url(self, url):
        """Navigate to a specific URL."""
        self.driver.get(url)

    def find_element(self, locator):
        """Wait for an element to be present in the DOM and return it."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Wait for elements to be present in the DOM and return them."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """Wait for an element to be clickable and then click it."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator, text):
        """Wait for an element to be visible, clear it, and type text."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Wait for an element to be visible and return its text content."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def is_element_visible(self, locator, timeout=5):
        """
        Check if an element is visible on the page within a specific timeout.
        Returns True if visible, False otherwise.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
