-- ============================================================
-- E-Commerce QA Project — Sample Data
-- 15 realistic products across 4 categories
-- ============================================================

USE ecommerce_qa;

-- Clear existing sample data (safe for re-runs)
DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM cart_items;
DELETE FROM cart;
DELETE FROM products;

-- ============================================================
-- Electronics (4 products)
-- ============================================================
INSERT INTO products (name, description, price, category, quantity, image_url) VALUES
('Wireless Bluetooth Headphones', 'Premium noise-cancelling wireless headphones with 30-hour battery life, comfortable over-ear design, and deep bass. Compatible with all Bluetooth devices.', 79.99, 'Electronics', 50, '/static/images/wireless-bluetooth-headphones.jpg'),
('USB-C Fast Charger 65W', 'Universal 65W USB-C power adapter with GaN technology. Fast charges laptops, tablets, and phones. Compact and travel-friendly design.', 34.99, 'Electronics', 120, '/static/images/usb-c-fast-charger-65w.jpg'),
('Mechanical Gaming Keyboard', 'RGB backlit mechanical keyboard with Cherry MX Blue switches, programmable keys, and aircraft-grade aluminum frame. Perfect for gaming and typing.', 129.99, 'Electronics', 35, '/static/images/mechanical-gaming-keyboard.jpg'),
('Portable Bluetooth Speaker', 'Waterproof portable speaker with 360-degree sound, 12-hour playtime, and built-in microphone for calls. Pairs with any Bluetooth device.', 49.99, 'Electronics', 80, '/static/images/portable-bluetooth-speaker.jpg');

-- ============================================================
-- Clothing (4 products)
-- ============================================================
INSERT INTO products (name, description, price, category, quantity, image_url) VALUES
('Classic Cotton T-Shirt', '100% organic cotton crew neck t-shirt. Pre-shrunk fabric, reinforced stitching, and available in multiple colors. Comfortable everyday wear.', 24.99, 'Clothing', 200, '/static/images/classic-cotton-tshirt.jpg'),
('Slim Fit Denim Jeans', 'Modern slim fit jeans crafted from premium stretch denim. Five-pocket styling with a comfortable mid-rise waist. Machine washable.', 59.99, 'Clothing', 150, '/static/images/slim-fit-denim-jeans.jpg'),
('Hooded Zip-Up Sweatshirt', 'Warm fleece-lined hoodie with full-length zipper, kangaroo pockets, and adjustable drawstring hood. Ideal for cool weather layering.', 44.99, 'Clothing', 100, '/static/images/hooded-zip-up-sweatshirt.jpg'),
('Running Athletic Shoes', 'Lightweight running shoes with responsive cushioning, breathable mesh upper, and non-slip rubber outsole. Engineered for comfort during long runs.', 89.99, 'Clothing', 75, '/static/images/running-athletic-shoes.jpg');

-- ============================================================
-- Books (4 products)
-- ============================================================
INSERT INTO products (name, description, price, category, quantity, image_url) VALUES
('Python Programming Fundamentals', 'Comprehensive guide to Python programming covering basics to advanced topics. Includes hands-on exercises, real-world projects, and best practices for beginners.', 39.99, 'Books', 60, '/static/images/python-programming-fundamentals.jpg'),
('The Art of Software Testing', 'Classic textbook on software testing methodologies. Covers unit testing, integration testing, system testing, and acceptance testing with practical examples.', 45.99, 'Books', 40, '/static/images/art-of-software-testing.jpg'),
('Data Structures and Algorithms', 'In-depth exploration of data structures and algorithms with implementations in Python and Java. Includes complexity analysis and interview preparation.', 54.99, 'Books', 30, '/static/images/data-structures-algorithms.jpg'),
('Clean Code: A Handbook', 'A guide to writing readable, maintainable, and efficient code. Learn naming conventions, function design, error handling, and refactoring techniques.', 42.99, 'Books', 55, '/static/images/clean-code-handbook.jpg');

-- ============================================================
-- Home & Kitchen (3 products)
-- ============================================================
INSERT INTO products (name, description, price, category, quantity, image_url) VALUES
('Stainless Steel Water Bottle', 'Double-wall vacuum insulated water bottle keeps drinks cold for 24 hours or hot for 12 hours. BPA-free, leak-proof cap, and eco-friendly design.', 27.99, 'Home & Kitchen', 180, '/static/images/stainless-steel-water-bottle.jpg'),
('Non-Stick Cooking Pan Set', 'Set of 3 premium non-stick frying pans (8", 10", 12"). PFOA-free coating, ergonomic handles, and oven-safe up to 450°F. Dishwasher safe.', 69.99, 'Home & Kitchen', 45, '/static/images/non-stick-cooking-pan-set.jpg'),
('LED Desk Lamp with USB Port', 'Adjustable LED desk lamp with 5 brightness levels, 3 color temperatures, and built-in USB charging port. Touch control and memory function.', 36.99, 'Home & Kitchen', 90, '/static/images/led-desk-lamp-usb.jpg');

-- Verify inserted data
SELECT CONCAT('Products inserted: ', COUNT(*)) AS status FROM products;
SELECT category, COUNT(*) AS count, ROUND(AVG(price), 2) AS avg_price FROM products GROUP BY category;
