"""
E-Commerce QA Project — Database Connection Helper
Provides MySQL connection management using mysql-connector-python.
"""

import mysql.connector
from mysql.connector import Error
from app.config import Config


def get_db_connection():
    """
    Create and return a new MySQL database connection.

    Returns:
        mysql.connector.connection.MySQLConnection: Active database connection.

    Raises:
        mysql.connector.Error: If connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def init_db():
    """
    Test database connectivity on application startup.
    Prints connection status to console.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        print("[OK] Database connection successful")
    except Error as e:
        print(f"[ERROR] Database connection failed: {e}")
        print("  Make sure MySQL is running and .env credentials are correct.")
