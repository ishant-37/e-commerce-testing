"""
Order Routes — Checkout, order placement, and order history.
Provides both JSON API endpoints and HTML page routes.
"""

from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for

from app.models import order as order_model
from app.models import cart as cart_model

orders_bp = Blueprint('orders', __name__)


def login_required_api():
    """Check if user is logged in for API requests."""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required. Please log in.'}), 401
    return None


# ============================================================
# HTML Page Routes
# ============================================================

@orders_bp.route('/checkout')
def checkout_page():
    """Render the checkout page."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))

    items = cart_model.get_cart_items(session['user_id'])
    total = cart_model.get_cart_total(session['user_id'])

    if not items:
        return redirect(url_for('cart.cart_page'))

    # Convert Decimal to float for template
    for item in items:
        item['price'] = float(item['price'])
        item['subtotal'] = float(item['subtotal'])

    return render_template('checkout.html', items=items, total=float(total))


@orders_bp.route('/orders')
def orders_page():
    """Render the order history page."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))

    orders = order_model.get_orders(session['user_id'])

    # Convert Decimal to float for template
    for order in orders:
        order['total_amount'] = float(order['total_amount'])

    return render_template('orders.html', orders=orders)


@orders_bp.route('/orders/<int:order_id>')
def order_detail_page(order_id):
    """Render the order detail page."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))

    order = order_model.get_order_by_id(order_id, session['user_id'])
    if not order:
        return render_template('404.html', message='Order not found'), 404

    # Convert Decimal to float for template
    order['total_amount'] = float(order['total_amount'])
    for item in order['items']:
        item['price'] = float(item['price'])
        item['subtotal'] = float(item['subtotal'])

    return render_template('order_detail.html', order=order)


@orders_bp.route('/order-confirmation/<int:order_id>')
def order_confirmation_page(order_id):
    """Render the order confirmation page after successful checkout."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))

    order = order_model.get_order_by_id(order_id, session['user_id'])
    if not order:
        return redirect(url_for('orders.orders_page'))

    # Convert Decimal to float for template
    order['total_amount'] = float(order['total_amount'])
    for item in order['items']:
        item['price'] = float(item['price'])
        item['subtotal'] = float(item['subtotal'])

    return render_template('order_confirmation.html', order=order)


# ============================================================
# REST API Endpoints
# ============================================================

@orders_bp.route('/api/orders', methods=['POST'])
def api_create_order():
    """
    Place an order from the user's cart.

    Request Body (JSON):
        shipping_name (str): Recipient name (required)
        shipping_address (str): Street address (required)
        shipping_city (str): City (required)
        shipping_zip (str): ZIP code (required)
        shipping_phone (str): Phone number (required)

    Returns:
        201: Order created successfully.
        400: Validation error or empty cart.
        401: Not authenticated.
    """
    auth_error = login_required_api()
    if auth_error:
        return auth_error

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    # Validate required shipping fields
    required_fields = ['shipping_name', 'shipping_address', 'shipping_city', 'shipping_zip', 'shipping_phone']
    errors = []
    for field in required_fields:
        value = data.get(field, '').strip()
        if not value:
            errors.append(f'{field.replace("_", " ").title()} is required')

    if errors:
        return jsonify({'error': errors}), 400

    try:
        order_id = order_model.create_order(
            user_id=session['user_id'],
            shipping_name=data['shipping_name'].strip(),
            shipping_address=data['shipping_address'].strip(),
            shipping_city=data['shipping_city'].strip(),
            shipping_zip=data['shipping_zip'].strip(),
            shipping_phone=data['shipping_phone'].strip()
        )

        order = order_model.get_order_by_id(order_id, session['user_id'])

        # Convert Decimal to float
        order['total_amount'] = float(order['total_amount'])
        for item in order['items']:
            item['price'] = float(item['price'])
            item['subtotal'] = float(item['subtotal'])

        return jsonify({
            'message': 'Order placed successfully',
            'order': order
        }), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to place order: {str(e)}'}), 500


@orders_bp.route('/api/orders', methods=['GET'])
def api_get_orders():
    """
    Get the current user's order history.

    Returns:
        200: List of orders.
        401: Not authenticated.
    """
    auth_error = login_required_api()
    if auth_error:
        return auth_error

    orders = order_model.get_orders(session['user_id'])

    # Convert Decimal to float
    for order in orders:
        order['total_amount'] = float(order['total_amount'])

    return jsonify({
        'orders': orders,
        'count': len(orders)
    }), 200


@orders_bp.route('/api/orders/<int:order_id>', methods=['GET'])
def api_get_order(order_id):
    """
    Get details of a specific order.

    Returns:
        200: Order details with items.
        401: Not authenticated.
        404: Order not found.
    """
    auth_error = login_required_api()
    if auth_error:
        return auth_error

    order = order_model.get_order_by_id(order_id, session['user_id'])
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # Convert Decimal to float
    order['total_amount'] = float(order['total_amount'])
    for item in order['items']:
        item['price'] = float(item['price'])
        item['subtotal'] = float(item['subtotal'])

    return jsonify({'order': order}), 200
