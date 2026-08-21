"""
Auth Routes — Registration, Login, and Logout.
Provides both JSON API endpoints and HTML page routes.
"""

import re
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash

from app.models import user as user_model

auth_bp = Blueprint('auth', __name__)


# ============================================================
# HTML Page Routes
# ============================================================

@auth_bp.route('/register', methods=['GET'])
def register_page():
    """Render the registration page."""
    if 'user_id' in session:
        return redirect(url_for('products.products_page'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET'])
def login_page():
    """Render the login page."""
    if 'user_id' in session:
        return redirect(url_for('products.products_page'))
    return render_template('login.html')


# ============================================================
# REST API Endpoints
# ============================================================

@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    """
    Register a new user.

    Request Body (JSON):
        name (str): Full name (required)
        email (str): Email address (required, must be valid format)
        password (str): Password (required, min 6 characters)

    Returns:
        201: User created successfully
        400: Validation error (missing fields, invalid email, weak password, duplicate email)
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    # Validation
    errors = []
    if not name:
        errors.append('Name is required')
    if not email:
        errors.append('Email is required')
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors.append('Invalid email format')
    if not password:
        errors.append('Password is required')
    elif len(password) < 6:
        errors.append('Password must be at least 6 characters')

    if errors:
        return jsonify({'error': errors}), 400

    # Check for duplicate email
    existing = user_model.find_by_email(email)
    if existing:
        return jsonify({'error': 'Email already registered'}), 400

    try:
        user_id = user_model.create_user(name, email, password)
        return jsonify({
            'message': 'Registration successful',
            'user': {'id': user_id, 'name': name, 'email': email}
        }), 201
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    """
    Log in a user.

    Request Body (JSON):
        email (str): Registered email (required)
        password (str): Password (required)

    Returns:
        200: Login successful (sets session)
        400: Missing fields
        401: Invalid credentials
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    email = data.get('email', '').strip()
    password = data.get('password', '')

    # Validation
    errors = []
    if not email:
        errors.append('Email is required')
    if not password:
        errors.append('Password is required')

    if errors:
        return jsonify({'error': errors}), 400

    # Find user
    user = user_model.find_by_email(email)
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    # Verify password
    if not user_model.verify_password(user['password'], password):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Set session
    session['user_id'] = user['id']
    session['user_name'] = user['name']
    session['user_email'] = user['email']

    return jsonify({
        'message': 'Login successful',
        'user': {'id': user['id'], 'name': user['name'], 'email': user['email']}
    }), 200


@auth_bp.route('/api/logout', methods=['POST'])
def api_logout():
    """
    Log out the current user.

    Returns:
        200: Logout successful (clears session)
    """
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200
