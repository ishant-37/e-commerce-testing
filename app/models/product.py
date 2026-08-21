"""
Product Model — Handles product listing, search, filtering, and detail retrieval.
"""

from app.database import get_db_connection


def get_all(search=None, category=None):
    """
    Get all products, optionally filtered by search term and/or category.

    Args:
        search (str, optional): Search term to match against product name/description.
        category (str, optional): Category to filter by.

    Returns:
        list[dict]: List of product records.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM products WHERE 1=1"
        params = []

        if search:
            query += " AND (name LIKE %s OR description LIKE %s)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term])

        if category:
            query += " AND category = %s"
            params.append(category)

        query += " ORDER BY id ASC"

        cursor.execute(query, params)
        products = cursor.fetchall()
        return products
    finally:
        cursor.close()
        conn.close()


def get_by_id(product_id):
    """
    Get a single product by its ID.

    Args:
        product_id (int): The product ID.

    Returns:
        dict or None: Product record or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        return product
    finally:
        cursor.close()
        conn.close()


def get_categories():
    """
    Get all distinct product categories.

    Returns:
        list[str]: List of category names.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        return categories
    finally:
        cursor.close()
        conn.close()
