"""
E-Commerce QA Project — Database Connection Helper
Uses SQLite for zero-config local development.
Database file is stored in the project root as 'ecommerce_qa.db'.
"""

import os
import sqlite3


# Database file path (in project root)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ecommerce_qa.db')


def get_db_connection():
    """
    Create and return a new SQLite database connection.
    Uses Row factory so rows behave like dicts.

    Returns:
        sqlite3.Connection: Active database connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def dict_from_row(row):
    """Convert a sqlite3.Row to a plain dict."""
    if row is None:
        return None
    return dict(row)


def dicts_from_rows(rows):
    """Convert a list of sqlite3.Row to a list of dicts."""
    return [dict(row) for row in rows]


def init_db():
    """
    Initialize the SQLite database: create tables and seed product data
    if the database is empty.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create tables
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                image_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS cart_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cart_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (cart_id) REFERENCES cart(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                shipping_name TEXT,
                shipping_address TEXT,
                shipping_city TEXT,
                shipping_zip TEXT,
                shipping_phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            );
        """)

        # Seed products if table is empty
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]

        if count == 0:
            products = [
                # Electronics
                ('Wireless Bluetooth Headphones', 'Premium noise-cancelling wireless headphones with 30-hour battery life, comfortable over-ear design, and deep bass. Compatible with all Bluetooth devices.', 79.99, 'Electronics', 50, '/static/images/wireless-bluetooth-headphones.jpg'),
                ('USB-C Fast Charger 65W', 'Universal 65W USB-C power adapter with GaN technology. Fast charges laptops, tablets, and phones. Compact and travel-friendly design.', 34.99, 'Electronics', 120, '/static/images/usb-c-fast-charger-65w.jpg'),
                ('Mechanical Gaming Keyboard', 'RGB backlit mechanical keyboard with Cherry MX Blue switches, programmable keys, and aircraft-grade aluminum frame. Perfect for gaming and typing.', 129.99, 'Electronics', 35, '/static/images/mechanical-gaming-keyboard.jpg'),
                ('Portable Bluetooth Speaker', 'Waterproof portable speaker with 360-degree sound, 12-hour playtime, and built-in microphone for calls. Pairs with any Bluetooth device.', 49.99, 'Electronics', 80, '/static/images/portable-bluetooth-speaker.jpg'),
                # Clothing
                ('Classic Cotton T-Shirt', '100% organic cotton crew neck t-shirt. Pre-shrunk fabric, reinforced stitching, and available in multiple colors. Comfortable everyday wear.', 24.99, 'Clothing', 200, '/static/images/classic-cotton-tshirt.jpg'),
                ('Slim Fit Denim Jeans', 'Modern slim fit jeans crafted from premium stretch denim. Five-pocket styling with a comfortable mid-rise waist. Machine washable.', 59.99, 'Clothing', 150, '/static/images/slim-fit-denim-jeans.jpg'),
                ('Hooded Zip-Up Sweatshirt', 'Warm fleece-lined hoodie with full-length zipper, kangaroo pockets, and adjustable drawstring hood. Ideal for cool weather layering.', 44.99, 'Clothing', 100, '/static/images/hooded-zip-up-sweatshirt.jpg'),
                ('Running Athletic Shoes', 'Lightweight running shoes with responsive cushioning, breathable mesh upper, and non-slip rubber outsole. Engineered for comfort during long runs.', 89.99, 'Clothing', 75, '/static/images/running-athletic-shoes.jpg'),
                # Books
                ('Python Programming Fundamentals', 'Comprehensive guide to Python programming covering basics to advanced topics. Includes hands-on exercises, real-world projects, and best practices for beginners.', 39.99, 'Books', 60, '/static/images/python-programming-fundamentals.jpg'),
                ('The Art of Software Testing', 'Classic textbook on software testing methodologies. Covers unit testing, integration testing, system testing, and acceptance testing with practical examples.', 45.99, 'Books', 40, '/static/images/art-of-software-testing.jpg'),
                ('Data Structures and Algorithms', 'In-depth exploration of data structures and algorithms with implementations in Python and Java. Includes complexity analysis and interview preparation.', 54.99, 'Books', 30, '/static/images/data-structures-algorithms.jpg'),
                ('Clean Code: A Handbook', 'A guide to writing readable, maintainable, and efficient code. Learn naming conventions, function design, error handling, and refactoring techniques.', 42.99, 'Books', 55, '/static/images/clean-code-handbook.jpg'),
                # Home & Kitchen
                ('Stainless Steel Water Bottle', 'Double-wall vacuum insulated water bottle keeps drinks cold for 24 hours or hot for 12 hours. BPA-free, leak-proof cap, and eco-friendly design.', 27.99, 'Home & Kitchen', 180, '/static/images/stainless-steel-water-bottle.jpg'),
                ('Non-Stick Cooking Pan Set', 'Set of 3 premium non-stick frying pans (8", 10", 12"). PFOA-free coating, ergonomic handles, and oven-safe up to 450°F. Dishwasher safe.', 69.99, 'Home & Kitchen', 45, '/static/images/non-stick-cooking-pan-set.jpg'),
                ('LED Desk Lamp with USB Port', 'Adjustable LED desk lamp with 5 brightness levels, 3 color temperatures, and built-in USB charging port. Touch control and memory function.', 36.99, 'Home & Kitchen', 90, '/static/images/led-desk-lamp-usb.jpg'),
            ]

            cursor.executemany(
                "INSERT INTO products (name, description, price, category, quantity, image_url) VALUES (?, ?, ?, ?, ?, ?)",
                products
            )
            conn.commit()
            print(f"[OK] Seeded {len(products)} products into database")

        conn.close()
        print("[OK] Database connection successful (SQLite)")
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")
        raise
