from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage

class ProductsPage(BasePage):
    """Page Object for the Products listing page."""
    
    # Locators
    SEARCH_INPUT = (By.ID, "search-input")
    SEARCH_BUTTON = (By.ID, "btn-search")
    CATEGORY_FILTER = (By.ID, "category-filter")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-card")
    CLEAR_FILTERS_BTN = (By.ID, "btn-clear-filters")
    NO_PRODUCTS_MSG = (By.ID, "no-products-message")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:5050/products"

    def navigate(self):
        """Navigate to the products page."""
        self.open_url(self.url)

    def search_for_product(self, search_term):
        """Enter a search term and submit."""
        self.type_text(self.SEARCH_INPUT, search_term)
        self.click(self.SEARCH_BUTTON)

    def filter_by_category(self, category_name):
        """Select a category from the dropdown."""
        # A simple click on the option works for standard selects
        category_option = (By.XPATH, f"//select[@id='category-filter']/option[text()='{category_name}']")
        self.click(self.CATEGORY_FILTER)
        self.click(category_option)

    def get_product_count(self):
        """Return the number of product cards currently displayed."""
        if self.is_element_visible((By.CSS_SELECTOR, ".product-card"), timeout=3):
             elements = self.find_elements(self.PRODUCT_CARDS)
             return len(elements)
        return 0

    def click_first_product_view_details(self):
        """Click the 'View Details' button of the first product in the grid."""
        first_view_btn = (By.CSS_SELECTOR, ".product-card:first-child a[id^='btn-view-']")
        self.click(first_view_btn)


class ProductDetailPage(BasePage):
    """Page Object for the Product Detail page."""
    
    # Locators
    PRODUCT_NAME = (By.ID, "product-name")
    PRODUCT_PRICE = (By.ID, "product-price")
    QUANTITY_INPUT = (By.ID, "quantity")
    ADD_TO_CART_BTN = (By.ID, "btn-add-to-cart")
    BACK_LINK = (By.ID, "back-to-products")
    FLASH_MESSAGE = (By.CSS_SELECTOR, ".flash")

    def get_product_name(self):
        return self.get_text(self.PRODUCT_NAME)
        
    def add_to_cart(self, quantity=1):
        """Set quantity and click Add to Cart."""
        if quantity != 1:
            self.type_text(self.QUANTITY_INPUT, str(quantity))
        self.click(self.ADD_TO_CART_BTN)

    def go_back_to_products(self):
        self.click(self.BACK_LINK)
        
    def get_flash_message(self):
        if self.is_element_visible(self.FLASH_MESSAGE, timeout=3):
            return self.get_text(self.FLASH_MESSAGE)
        return None
