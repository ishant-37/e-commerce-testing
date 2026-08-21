"""
E-Commerce QA Project — Flask Application Entry Point
Creates and configures the Flask application, registers all blueprints.
"""

from flask import Flask
from app.config import Config
from app.database import init_db


def create_app():
    """
    Application factory — creates and configures the Flask app.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY

    # Test database connection on startup
    with app.app_context():
        init_db()

    # Register blueprints (route groups)
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import orders_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)

    # Custom error handlers
    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template, request, jsonify
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Resource not found'}), 404
        return render_template('404.html', message='Page not found'), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import request, jsonify
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error'}), 500
        return '<h1>500 — Internal Server Error</h1>', 500

    return app


# Run directly: python app/app.py
if __name__ == '__main__':
    app = create_app()
    print("\n" + "=" * 50)
    print("  E-Commerce QA Project")
    print("  Running at: http://localhost:5000")
    print("=" * 50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
