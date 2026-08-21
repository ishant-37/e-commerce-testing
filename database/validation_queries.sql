-- ============================================================
-- E-Commerce QA Project — Database Validation Queries
-- Used for validating backend data integrity during manual/auth testing
-- ============================================================

USE ecommerce_qa;

-- 1. Validate User Registration
-- Checks if a specific user email was registered successfully.
SELECT id, name, email, created_at
FROM users
WHERE email = 'testuser@example.com';

-- 2. Validate Login-related Data
-- Retrieves the password hash for a registered email (to confirm encryption).
SELECT email, password
FROM users
WHERE email = 'testuser@example.com';

-- 3. Validate Product Catalog
-- Lists all products with their categories, prices, and stock levels.
SELECT id, name, category, price, quantity
FROM products;

-- 4. Validate User's Cart
-- Shows all products currently in a user's cart along with quantities, prices, and calculated subtotals.
SELECT
    c.id AS cart_id,
    c.user_id,
    ci.id AS item_id,
    p.name AS product_name,
    ci.quantity,
    p.price AS unit_price,
    (ci.quantity * p.price) AS subtotal
FROM cart c
JOIN cart_items ci ON c.id = ci.cart_id
JOIN products p ON ci.product_id = p.id
WHERE c.user_id = 1; -- Replace with actual User ID

-- 5. Calculate Cart Total (Expected Order Value)
-- Sums up the subtotals in the cart.
SELECT
    c.user_id,
    SUM(ci.quantity * p.price) AS calculated_total
FROM cart c
JOIN cart_items ci ON c.id = ci.cart_id
JOIN products p ON ci.product_id = p.id
WHERE c.user_id = 1 -- Replace with actual User ID
GROUP BY c.user_id;

-- 6. Validate Order Placement (Header Level)
-- Checks the order record created after checkout.
SELECT id, user_id, total_amount, status, shipping_name, shipping_address, shipping_phone, created_at
FROM orders
WHERE user_id = 1 -- Replace with actual User ID
ORDER BY created_at DESC;

-- 7. Validate Order Details (Items Level)
-- Shows all products purchased in a specific order, their quantities, purchase prices, and calculated totals.
SELECT
    o.id AS order_id,
    oi.id AS item_id,
    p.name AS product_name,
    oi.quantity,
    oi.price AS purchase_price,
    (oi.quantity * oi.price) AS subtotal
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.id = 1; -- Replace with actual Order ID

-- 8. Verify Order Total Matches Sum of Order Items
-- Cross-check to ensure header total_amount matches the sum of detailed order items.
SELECT
    o.id AS order_id,
    o.total_amount AS header_total,
    SUM(oi.quantity * oi.price) AS items_sum,
    (o.total_amount - SUM(oi.quantity * oi.price)) AS difference
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
WHERE o.id = 1 -- Replace with actual Order ID
GROUP BY o.id, o.total_amount;

-- 9. Check Product Inventory After Purchase
-- Asserts that product stock levels are adjusted if inventory deduction is implemented.
SELECT id, name, quantity AS current_stock
FROM products
WHERE id IN (1, 2); -- Replace with product IDs purchased
