"""
User Model — Handles user registration, login, and lookup.
Uses werkzeug.security for password hashing (bcrypt-style).
"""

from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db_connection, dict_from_row


def create_user(name, email, password):
    """
    Register a new user.

    Args:
        name (str): Full name of the user.
        email (str): Email address (must be unique).
        password (str): Plain-text password (will be hashed).

    Returns:
        int: The new user's ID.

    Raises:
        Exception: If the email already exists or DB error occurs.
    """
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    finally:
        conn.close()


def find_by_email(email):
    """
    Look up a user by email address.

    Args:
        email (str): Email to search for.

    Returns:
        dict or None: User record with keys (id, name, email, password, created_at),
                      or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = dict_from_row(cursor.fetchone())
        return user
    finally:
        conn.close()


def find_by_id(user_id):
    """
    Look up a user by ID.

    Args:
        user_id (int): User ID to search for.

    Returns:
        dict or None: User record or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = ?", (user_id,))
        user = dict_from_row(cursor.fetchone())
        return user
    finally:
        conn.close()


def verify_password(stored_password, provided_password):
    """
    Verify a plain-text password against a stored hash.

    Args:
        stored_password (str): The hashed password from the database.
        provided_password (str): The plain-text password to check.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return check_password_hash(stored_password, provided_password)
