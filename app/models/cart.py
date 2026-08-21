"""
Cart Model — Handles cart creation, adding/updating/removing items, and cart retrieval.
Each user gets one cart (created on first add-to-cart).
"""

from app.database import get_db_connection, dict_from_row, dicts_from_rows


def get_or_create_cart(user_id):
    """
    Get the user's cart ID. Creates a new cart if one doesn't exist.

    Args:
        user_id (int): The logged-in user's ID.

    Returns:
        int: The cart ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM cart WHERE user_id = ?", (user_id,))
        cart = cursor.fetchone()
        if cart:
            return cart['id']

        # Create new cart
        cursor.execute("INSERT INTO cart (user_id) VALUES (?)", (user_id,))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_cart_items(user_id):
    """
    Get all items in the user's cart with product details.

    Args:
        user_id (int): The logged-in user's ID.

    Returns:
        list[dict]: Cart items with product name, price, quantity, and subtotal.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT ci.id, ci.cart_id, ci.product_id, ci.quantity,
                   p.name, p.price, p.image_url,
                   (ci.quantity * p.price) AS subtotal
            FROM cart_items ci
            JOIN cart c ON ci.cart_id = c.id
            JOIN products p ON ci.product_id = p.id
            WHERE c.user_id = ?
            ORDER BY ci.id ASC
        """
        cursor.execute(query, (user_id,))
        items = dicts_from_rows(cursor.fetchall())
        return items
    finally:
        conn.close()


def get_cart_total(user_id):
    """
    Calculate the total price of all items in the user's cart.

    Args:
        user_id (int): The logged-in user's ID.

    Returns:
        float: Total cart value.
    """
    items = get_cart_items(user_id)
    total = sum(float(item['subtotal']) for item in items)
    return round(total, 2)


def add_item(user_id, product_id, quantity=1):
    """
    Add a product to the cart. If the product is already in the cart,
    increment its quantity.

    Args:
        user_id (int): User ID.
        product_id (int): Product ID to add.
        quantity (int): Quantity to add (default 1).

    Returns:
        dict: The cart item record.
    """
    cart_id = get_or_create_cart(user_id)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if product already in cart
        cursor.execute(
            "SELECT id, quantity FROM cart_items WHERE cart_id = ? AND product_id = ?",
            (cart_id, product_id)
        )
        existing = cursor.fetchone()

        if existing:
            existing = dict(existing)
            new_qty = existing['quantity'] + quantity
            cursor.execute(
                "UPDATE cart_items SET quantity = ? WHERE id = ?",
                (new_qty, existing['id'])
            )
            conn.commit()
            return {'id': existing['id'], 'cart_id': cart_id, 'product_id': product_id, 'quantity': new_qty}
        else:
            cursor.execute(
                "INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (?, ?, ?)",
                (cart_id, product_id, quantity)
            )
            conn.commit()
            return {'id': cursor.lastrowid, 'cart_id': cart_id, 'product_id': product_id, 'quantity': quantity}
    finally:
        conn.close()


def update_item(item_id, quantity, user_id):
    """
    Update the quantity of a cart item. Removes the item if quantity <= 0.

    Args:
        item_id (int): Cart item ID.
        quantity (int): New quantity.
        user_id (int): User ID (for authorization check).

    Returns:
        bool: True if updated, False if item not found or unauthorized.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Verify the item belongs to this user
        cursor.execute("""
            SELECT ci.id FROM cart_items ci
            JOIN cart c ON ci.cart_id = c.id
            WHERE ci.id = ? AND c.user_id = ?
        """, (item_id, user_id))
        item = cursor.fetchone()
        if not item:
            return False

        if quantity <= 0:
            cursor.execute("DELETE FROM cart_items WHERE id = ?", (item_id,))
        else:
            cursor.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (quantity, item_id))

        conn.commit()
        return True
    finally:
        conn.close()


def remove_item(item_id, user_id):
    """
    Remove an item from the cart.

    Args:
        item_id (int): Cart item ID.
        user_id (int): User ID (for authorization check).

    Returns:
        bool: True if removed, False if not found or unauthorized.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT ci.id FROM cart_items ci
            JOIN cart c ON ci.cart_id = c.id
            WHERE ci.id = ? AND c.user_id = ?
        """, (item_id, user_id))
        item = cursor.fetchone()
        if not item:
            return False

        cursor.execute("DELETE FROM cart_items WHERE id = ?", (item_id,))
        conn.commit()
        return True
    finally:
        conn.close()


def clear_cart(user_id):
    """
    Remove all items from the user's cart.

    Args:
        user_id (int): User ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # SQLite doesn't support DELETE with JOIN, use subquery instead
        cursor.execute("""
            DELETE FROM cart_items WHERE cart_id IN (
                SELECT id FROM cart WHERE user_id = ?
            )
        """, (user_id,))
        conn.commit()
    finally:
        conn.close()
