from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage

class CartPage(BasePage):
    """Page Object for the Shopping Cart page."""
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")
    CHECKOUT_BUTTON = (By.ID, "btn-checkout")
    EMPTY_CART_MESSAGE = (By.ID, "empty-cart-message")
    CLEAR_CART_BUTTON = (By.ID, "btn-clear-cart")
    TOTAL_PRICE = (By.ID, "cart-total")
    FLASH_MESSAGE = (By.CSS_SELECTOR, ".flash")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:5050/cart"

    def navigate(self):
        self.open_url(self.url)

    def get_cart_item_count(self):
        """Return the number of unique items in the cart."""
        if self.is_element_visible(self.CART_ITEMS, timeout=3):
            return len(self.find_elements(self.CART_ITEMS))
        return 0

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        
    def clear_cart(self):
        if self.is_element_visible(self.CLEAR_CART_BUTTON, timeout=2):
             self.click(self.CLEAR_CART_BUTTON)
             
    def get_flash_message(self):
        if self.is_element_visible(self.FLASH_MESSAGE, timeout=3):
            return self.get_text(self.FLASH_MESSAGE)
        return None


class CheckoutPage(BasePage):
    """Page Object for the Checkout page."""
    
    # Locators
    NAME_INPUT = (By.ID, "shipping_name")
    ADDRESS_INPUT = (By.ID, "shipping_address")
    CITY_INPUT = (By.ID, "shipping_city")
    ZIP_CODE_INPUT = (By.ID, "shipping_zip")
    PHONE_INPUT = (By.ID, "shipping_phone")
    PLACE_ORDER_BUTTON = (By.ID, "btn-place-order")
    FLASH_MESSAGE = (By.CSS_SELECTOR, ".flash")

    def fill_shipping_details(self, name, address, city, zip_code, phone):
        self.type_text(self.NAME_INPUT, name)
        self.type_text(self.ADDRESS_INPUT, address)
        self.type_text(self.CITY_INPUT, city)
        self.type_text(self.ZIP_CODE_INPUT, zip_code)
        self.type_text(self.PHONE_INPUT, phone)

    def place_order(self):
        self.click(self.PLACE_ORDER_BUTTON)
        
    def get_flash_message(self):
        if self.is_element_visible(self.FLASH_MESSAGE, timeout=3):
            return self.get_text(self.FLASH_MESSAGE)
        return None
