"""
Product Routes — Product listing, search, filtering, and detail views.
Provides both JSON API endpoints and HTML page routes.
"""

from flask import Blueprint, request, jsonify, render_template

from app.models import product as product_model

products_bp = Blueprint('products', __name__)


# ============================================================
# HTML Page Routes
# ============================================================

@products_bp.route('/')
@products_bp.route('/products')
def products_page():
    """Render the product listing page with search and filter support."""
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    products = product_model.get_all(search=search or None, category=category or None)
    categories = product_model.get_categories()

    return render_template('products.html',
                           products=products,
                           categories=categories,
                           current_search=search,
                           current_category=category)


@products_bp.route('/products/<int:product_id>')
def product_detail_page(product_id):
    """Render the product detail page."""
    product = product_model.get_by_id(product_id)
    if not product:
        return render_template('404.html', message='Product not found'), 404
    return render_template('product_detail.html', product=product)


# ============================================================
# REST API Endpoints
# ============================================================

@products_bp.route('/api/products', methods=['GET'])
def api_get_products():
    """
    Get all products with optional search and category filter.

    Query Parameters:
        search (str, optional): Search term for name/description.
        category (str, optional): Filter by category name.

    Returns:
        200: List of products.
    """
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    products = product_model.get_all(search=search or None, category=category or None)

    # Convert Decimal to float for JSON serialization
    for p in products:
        p['price'] = float(p['price'])

    return jsonify({
        'products': products,
        'count': len(products)
    }), 200


@products_bp.route('/api/products/<int:product_id>', methods=['GET'])
def api_get_product(product_id):
    """
    Get a single product by ID.

    Returns:
        200: Product details.
        404: Product not found.
    """
    product = product_model.get_by_id(product_id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    product['price'] = float(product['price'])

    return jsonify({'product': product}), 200
