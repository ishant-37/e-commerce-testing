"""
Run the E-Commerce QA Flask application.
Usage: python run.py
"""

from app.app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  E-Commerce QA Project")
    print("  Running at: http://localhost:5050")
    print("=" * 50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5050)
