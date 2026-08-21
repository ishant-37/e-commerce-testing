import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to initialize the Selenium WebDriver before each test
    and close it after the test finishes.
    Using webdriver_manager to automatically download and manage the ChromeDriver.
    """
    # Set up Chrome options (e.g., run headful for visibility, or headless for CI)
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Uncomment to run invisibly
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize the WebDriver
    # ChromeDriverManager().install() automatically downloads the correct driver for the installed Chrome version
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Implicit wait as a fallback, though explicit waits in BasePage are preferred
    driver.implicitly_wait(5) 
    
    # Yield the driver to the test function
    yield driver
    
    # Teardown: Close the browser after the test completes
    driver.quit()
