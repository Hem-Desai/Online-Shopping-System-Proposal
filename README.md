Online Shopping System

A robust e-commerce backend system built with Python, featuring secure user authentication, product management, order processing, and more.

🌟 Features

Core Functionality

User Management

Customer registration and authentication

Role-based access control (Admin/Customer)

Secure password hashing with bcrypt

Product Management

Product CRUD operations

Inventory tracking

Product categorization

Order Processing

Shopping cart functionality

Order creation and tracking

Payment processing

Delivery status updates

Security Features

Password hashing (bcrypt)

Data encryption (Fernet)

Secure key management

Session handling

Database Structure

Customers

Products

Orders

Order Items

Payments

Deliveries

🚀 Getting Started

Prerequisites

# Required Python version
Python 3.8+

# Required packages
pip install -r requirements.txt

Installation

Clone the repository

git clone https://github.com/yourusername/online-shopping-system.git
cd online-shopping-system

Install dependencies

pip install -r requirements.txt

Initialize the database

python test_data.py

Configuration

Create a .env file in the root directory:

DB_NAME=shop.db
SECRET_KEY=your_secret_key

Ensure the encryption_key.key file is present in the root directory for secure data encryption. If not, it will be generated automatically during the first run.

📁 Project Structure

online-shopping-system/
├── database.py         # Database connection and operations
├── models.py          # Data models and repositories
├── security.py        # Security and encryption utilities
├── main.py           # Main application logic
├── test_data.py      # Test data initialization
├── requirements.txt   # Project dependencies
├── encryption_key.key # Encryption key for secure data
└── shop.db            # SQLite database file

🔧 Core Components

1. Database Connection (database.py)

SQLite database management

Connection pooling

Query execution

Error handling

2. Data Models (models.py)

@dataclass
class Customer:
    name: str
    email: str
    password_hash: str
    customer_id: Optional[int] = None
    created_at: datetime = datetime.now()
    is_admin: bool = False

@dataclass
class Product:
    name: str
    price: Decimal
    stock_quantity: int
    product_id: Optional[int] = None
    description: Optional[str] = None

3. Security Manager (security.py)

Password hashing with bcrypt

Data encryption with Fernet

Secure key management

Session handling

4. Main System (main.py)

User registration and authentication

Product management

Order processing

System initialization

🔐 Security Features

Password Security

Bcrypt hashing with salt

Minimum password requirements

Failed login attempt handling

Data Protection

AES encryption for sensitive data

Secure key storage

Session management

🛠️ Object-Oriented Design Principles

Encapsulation

Each class (e.g., Customer, Product, Order, SecurityManager) encapsulates its functionality and attributes.

Abstraction

High-level logic is abstracted in main.py, while low-level database and security operations are handled in dedicated files (database.py, security.py).

Modularity

The project is divided into distinct modules, each handling a specific responsibility (e.g., database operations, security, business logic).

Dependency Injection

Classes like CustomerRepository and ProductRepository accept dependencies (e.g., DatabaseConnection, SecurityManager) via their constructors, enabling better testability and flexibility.

Single Responsibility Principle

Each class and file focuses on a single responsibility, adhering to clean coding practices.

📝 Usage Examples

User Registration

shop = OnlineShoppingSystem()
success = shop.register_user(
    name="John Doe",
    email="john@example.com",
    password="SecurePass123!"
)

Product Management

# Add new product (admin only)
success = shop.add_product(
    name="Laptop Pro X",
    price=1299.99,
    quantity=10,
    description="High-performance laptop"
)

Order Processing

# Place order
order = shop.place_order(
    customer_id=1,
    products=[(1, 2), (3, 1)]  # (product_id, quantity)
)

🧪 Testing

Run the test data script to populate the database with sample data:

python test_data.py

🛠️ Future Enhancements

Shopping Cart System

Review & Rating System

Notification Service

Inventory Management

Discount System

API Integration

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

👥 Contributing

Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Create a Pull Request
