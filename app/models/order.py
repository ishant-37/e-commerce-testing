"""
Order Model — Handles order creation, retrieval, and order history.
Converts cart items into a permanent order record.
"""

from app.database import get_db_connection, dict_from_row, dicts_from_rows
from app.models import cart as cart_model


def create_order(user_id, shipping_name, shipping_address, shipping_city, shipping_zip, shipping_phone):
    """
    Create an order from the user's current cart.
    Transfers all cart items into order_items and clears the cart.

    Args:
        user_id (int): User ID.
        shipping_name (str): Recipient name.
        shipping_address (str): Street address.
        shipping_city (str): City.
        shipping_zip (str): ZIP/postal code.
        shipping_phone (str): Phone number.

    Returns:
        int: The new order ID.

    Raises:
        ValueError: If the cart is empty.
    """
    # Get cart items
    items = cart_model.get_cart_items(user_id)
    if not items:
        raise ValueError("Cart is empty. Cannot place order.")

    total_amount = cart_model.get_cart_total(user_id)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Create order
        cursor.execute("""
            INSERT INTO orders (user_id, total_amount, status, shipping_name, shipping_address,
                                shipping_city, shipping_zip, shipping_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, total_amount, 'Confirmed', shipping_name, shipping_address,
              shipping_city, shipping_zip, shipping_phone))
        order_id = cursor.lastrowid

        # Create order items
        for item in items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (order_id, item['product_id'], item['quantity'], float(item['price'])))

        conn.commit()

        # Clear the cart after successful order
        cart_model.clear_cart(user_id)

        return order_id
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_orders(user_id):
    """
    Get all orders for a user, most recent first.

    Args:
        user_id (int): User ID.

    Returns:
        list[dict]: List of order records.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, total_amount, status, created_at
            FROM orders WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        orders = dicts_from_rows(cursor.fetchall())
        return orders
    finally:
        conn.close()


def get_order_by_id(order_id, user_id):
    """
    Get a single order with its items.

    Args:
        order_id (int): Order ID.
        user_id (int): User ID (for authorization).

    Returns:
        dict or None: Order record with 'items' key, or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get order
        cursor.execute("""
            SELECT * FROM orders WHERE id = ? AND user_id = ?
        """, (order_id, user_id))
        row = cursor.fetchone()
        if not row:
            return None

        order = dict_from_row(row)

        # Get order items
        cursor.execute("""
            SELECT oi.id, oi.product_id, oi.quantity, oi.price,
                   p.name, p.image_url,
                   (oi.quantity * oi.price) AS subtotal
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        """, (order_id,))
        order['items'] = dicts_from_rows(cursor.fetchall())

        return order
    finally:
        conn.close()
