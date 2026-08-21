# E-Commerce QA Project...

A Flask and MySQL e-commerce application used as a hands-on QA project. The repository includes a small storefront, session-based authentication, product browsing, cart management, checkout and order history, REST-style JSON endpoints, database scripts, and spaces for automated and manual test assets.

## Features

- User registration, login, and logout
- Product catalog with search and category filtering
- Product detail pages
- Session-backed shopping cart
- Cart item add, update, and delete operations
- Checkout and order placement
- Order history, order details, and confirmation pages
- JSON API endpoints for application workflows
- MySQL schema, sample data, and validation queries
- Separate locations for API testing, browser automation, manual tests, reports, and screenshots

## Technology Stack

- Python 3.10+ recommended
- Flask 3.1.1
- MySQL 8.0+
- `mysql-connector-python`
- `python-dotenv`
- HTML templates, CSS, and JavaScript served by Flask

## Repository Structure

```text
Ecommerce-QA-Project/
|-- api-testing/postman/       Postman collection workspace
|-- app/                       Flask application
|   |-- models/                Database access for users, products, carts, and orders
|   |-- routes/                Authentication, product, cart, and order routes
|   |-- static/                 CSS, JavaScript, and image assets
|   `-- templates/              HTML pages
|-- automation/                Browser automation page objects and tests
|-- database/
|   |-- schema.sql              MySQL database and table definitions
|   |-- sample_data.sql         Sample product records
|   `-- validation_queries.sql  QA data-validation queries
|-- documentation/agile/       Agile and project documentation
|-- reports/                   Generated test reports
|-- screenshots/               Test screenshots
|-- tests/                     Manual and automation test locations
|-- .env                       Local configuration, not committed
|-- .gitignore
|-- requirements.txt
`-- README.md
```

## Prerequisites

Install the following before running the application:

1. Python 3.10 or newer
2. MySQL Server 8.0 or newer, running locally or on an accessible host
3. Git, if cloning the repository

## Installation

From the repository root, create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Database Setup

Create the database and tables with the schema script:

```bash
mysql -u root -p < database/schema.sql
```

Load the sample catalog:

```bash
mysql -u root -p ecommerce_qa < database/sample_data.sql
```

The sample data script is intended for a development or test database. It deletes existing cart, order, and product records before inserting the sample catalog.

## Environment Configuration

Create a local `.env` file in the repository root. The file is ignored by Git and should never contain credentials committed to the repository.

```dotenv
SECRET_KEY=replace-with-a-long-random-value
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_DATABASE=ecommerce_qa
```

The application defaults to `localhost`, port `3306`, user `root`, an empty password, and database `ecommerce_qa` when values are not provided. Use explicit values for shared or production-like environments.

## Run the Application

Start MySQL, activate the virtual environment, and run from the repository root:

```bash
python app/app.py
```

The application listens on:

```text
http://localhost:5000
```

The application checks the MySQL connection during startup. If startup reports a database connection failure, verify that MySQL is running and that `.env` contains the correct connection settings.

## Web Pages

| Method | Path | Description |
|---|---|---|
| GET | `/` | Product catalog |
| GET | `/products` | Product catalog with optional search and category filters |
| GET | `/products/<product_id>` | Product details |
| GET | `/register` | Registration page |
| GET | `/login` | Login page |
| GET | `/cart` | Current user's cart |
| GET | `/checkout` | Checkout form |
| GET | `/orders` | Current user's order history |
| GET | `/orders/<order_id>` | Order details |
| GET | `/order-confirmation/<order_id>` | Order confirmation |

## JSON API

All request bodies below use JSON. Authenticated endpoints use the Flask session created by `/api/login`.

| Method | Path | Description | Auth |
|---|---|---|---|
| POST | `/api/register` | Register a user with `name`, `email`, and `password` | No |
| POST | `/api/login` | Log in with `email` and `password` | No |
| POST | `/api/logout` | Clear the current session | No |
| GET | `/api/products` | List products; supports `search` and `category` query parameters | No |
| GET | `/api/products/<product_id>` | Get one product | No |
| GET | `/api/cart` | Get the current user's cart | Yes |
| POST | `/api/cart` | Add `product_id` and optional `quantity` | Yes |
| PUT | `/api/cart/<item_id>` | Update a cart item's `quantity` | Yes |
| DELETE | `/api/cart/<item_id>` | Remove a cart item | Yes |
| POST | `/api/orders` | Place an order with shipping fields | Yes |
| GET | `/api/orders` | Get the current user's order history | Yes |
| GET | `/api/orders/<order_id>` | Get one order and its items | Yes |

Example product request:

```bash
curl http://localhost:5000/api/products
```

Example registration request:

```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"QA User\",\"email\":\"qa@example.com\",\"password\":\"testing123\"}"
```

For authenticated API testing, keep the session cookie returned by `/api/login` in your API client and send it with subsequent cart and order requests. The Postman workspace is located in `api-testing/postman/`.

## QA Workflow

A typical exploratory or manual API test flow is:

1. Initialize MySQL with `database/schema.sql`.
2. Load products with `database/sample_data.sql`.
3. Start the Flask application.
4. Register a test user through the UI or `/api/register`.
5. Log in and retain the session cookie.
6. Browse products and test search/category filters.
7. Add, update, and remove cart items.
8. Place an order with valid shipping information.
9. Verify the order through `/orders` or `/api/orders`.
10. Run the relevant statements in `database/validation_queries.sql` to verify persisted data and totals.

The `tests/`, `automation/`, `reports/`, and `screenshots/` directories are organized for expanding this workflow with automated tests, manual test evidence, and generated results.

## Testing Status

The repository currently provides the application, database validation scripts, and test/automation directory structure. Add test cases and automation under their respective directories as coverage grows. No project-specific test runner command is currently defined in `requirements.txt`.

## Security Notes

- Do not commit `.env`, database passwords, session secrets, or generated test evidence containing sensitive data.
- Replace the development `SECRET_KEY` before deploying outside local development.
- Use a dedicated MySQL user with only the permissions required by the application.
- Run the sample data script only against a disposable development or test database.

## License

No license file is currently included in this repository.
