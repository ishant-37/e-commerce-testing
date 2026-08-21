"""
Cart Routes — Cart management (add, update, remove items).
Provides both JSON API endpoints and HTML page routes.
"""

from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for

from app.models import cart as cart_model

cart_bp = Blueprint('cart', __name__)


def login_required_api():
    """Check if user is logged in for API requests."""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required. Please log in.'}), 401
    return None


# ============================================================
# HTML Page Routes
# ============================================================

@cart_bp.route('/cart')
def cart_page():
    """Render the cart page."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))

    items = cart_model.get_cart_items(session['user_id'])
    total = cart_model.get_cart_total(session['user_id'])

    # Convert Decimal to float for template
    for item in items:
        item['price'] = float(item['price'])
        item['subtotal'] = float(item['subtotal'])

    return render_template('cart.html', items=items, total=float(total))


# ============================================================
# REST API Endpoints
# ============================================================

@cart_bp.route('/api/cart', methods=['GET'])
def api_get_cart():
    """
    Get the current user's cart items.

    Returns:
        200: Cart items and total.
        401: Not authenticated.
    """
    auth_error = login_required_api()
    if auth_error:
        return auth_error

    items = cart_model.get_cart_items(session['user_id'])
    total = cart_model.get_cart_total(session['user_id'])

    # Convert Decimal to float
    for item in items:
        item['price'] = float(item['price'])
        item['subtotal'] = float(item['subtotal'])

    return jsonify({
        'items': items,
        'total': float(total),
        'count': len(items)
    }), 200


@cart_bp.route('/api/cart', methods=['POST'])
def api_add_to_cart():
    """
    Add a product to the cart.

    Request Body (JSON):
        product_id (int): Product ID (required)
        quantity (int): Quantity to add (default 1)

    Returns:
        201: Item added to cart.
        400: Validation error.
        401: Not authenticated.
    """
    auth_error = login_required_api()
    if auth_error:
        return auth_error

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return jsonify({'error': 'product_id is required'}), 400

    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({'error': 'Quantity must be a positive integer'}), 400

    try:
        item = cart_model.add_item(session['user_id'], product_id, quantity)
        return jsonify({'message': 'Product added to cart', 'item': item}), 201
    except Exception as e:
        return jsonify({'error': f'Failed to add to cart: {str(e)}'}), 500


@cart_bp.route('/api/cart/<int:item_id>', methods=['PUT'])
def api_update_cart_item(item_id):
    """
    Update the quantity of a cart item.

    Request Body (JSON):
        quantity (int): New quantity (required, must be >= 1)

    Returns:
        200: Item updated.
        400: Validation error.
        401: Not authenticated.
        404: Item not found.
    """
    auth_error = login_required_api()
    if auth_error:
        return auth_error

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    quantity = data.get('quantity')
    if quantity is None:
        return jsonify({'error': 'quantity is required'}), 400
    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({'error': 'Quantity must be a positive integer'}), 400

    success = cart_model.update_item(item_id, quantity, session['user_id'])
    if not success:
        return jsonify({'error': 'Cart item not found'}), 404

    return jsonify({'message': 'Cart item updated', 'quantity': quantity}), 200


@cart_bp.route('/api/cart/<int:item_id>', methods=['DELETE'])
def api_remove_cart_item(item_id):
    """
    Remove an item from the cart.

    Returns:
        200: Item removed.
        401: Not authenticated.
        404: Item not found.
    """
    auth_error = login_required_api()
    if auth_error:
        return auth_error

    success = cart_model.remove_item(item_id, session['user_id'])
    if not success:
        return jsonify({'error': 'Cart item not found'}), 404

    return jsonify({'message': 'Item removed from cart'}), 200
