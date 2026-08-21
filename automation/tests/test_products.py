from automation.pages.product_pages import ProductsPage, ProductDetailPage

def test_view_all_products(driver):
    """Test that all products load on the main page."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    
    count = products_page.get_product_count()
    assert count == 15, f"Expected 15 products to be loaded, but found {count}"

def test_search_functionality(driver):
    """Test that searching for a product returns the correct results."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    
    products_page.search_for_product("Keyboard")
    count = products_page.get_product_count()
    assert count == 1, f"Expected 1 result for 'Keyboard', but got {count}"
    
    # Clear filters
    products_page.click(products_page.CLEAR_FILTERS_BTN)
    assert products_page.get_product_count() == 15, "Expected 15 products after clearing filters"

def test_category_filter(driver):
    """Test that filtering by category works correctly."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    
    products_page.filter_by_category("Clothing")
    count = products_page.get_product_count()
    assert count == 4, f"Expected 4 clothing items, but got {count}"

def test_product_detail_view(driver):
    """Test navigating to a product detail page."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    
    # Click the first product's details button
    products_page.click_first_product_view_details()
    
    # We should now be on the detail page
    detail_page = ProductDetailPage(driver)
    assert "Wireless Bluetooth Headphones" in detail_page.get_product_name(), "Product name mismatch on detail page"
