import time
from automation.pages.auth_pages import RegisterPage, LoginPage
from automation.pages.product_pages import ProductsPage, ProductDetailPage
from automation.pages.cart_pages import CartPage, CheckoutPage

def test_end_to_end_checkout_flow(driver):
    """
    Test the complete flow:
    1. Register/Login
    2. Add item to cart
    3. Proceed to checkout
    4. Place order
    """
    unique_email = f"buyer_{int(time.time())}@example.com"
    password = "BuyerPassword123!"

    # 1. Registration
    register_page = RegisterPage(driver)
    register_page.navigate()
    register_page.register("Jane Buyer", unique_email, password, password)
    time.sleep(2) # wait for redirect

    # 2. Login
    login_page = LoginPage(driver)
    login_page.navigate() # Force navigation to avoid JS redirect race condition
    login_page.login(unique_email, password)
    time.sleep(2) # wait for redirect to /products
    
    # 3. View Products & Add to Cart
    products_page = ProductsPage(driver)
    products_page.click_first_product_view_details()
    
    detail_page = ProductDetailPage(driver)
    detail_page.add_to_cart(quantity=2)
    
    flash_msg = detail_page.get_flash_message()
    assert "added to cart" in flash_msg.lower(), "Failed to add item to cart"
    
    # 4. View Cart
    cart_page = CartPage(driver)
    cart_page.navigate()
    assert cart_page.get_cart_item_count() >= 1, "Cart is empty"
    
    # 5. Checkout
    cart_page.proceed_to_checkout()
    time.sleep(1) # wait for redirect to /checkout
    
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_shipping_details("Jane Buyer", "123 Test Street", "Testville", "12345", "555-123-4567")
    checkout_page.place_order()
    
    # 6. Verify Order Success
    time.sleep(2) # Wait for processing and redirect to /order-confirmation/
    assert "/order-confirmation" in driver.current_url, "User not redirected to order confirmation page"
    assert "Order Placed Successfully" in driver.page_source, "Order placement failed, confirmation text not found"
