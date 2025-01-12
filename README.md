# Online Shopping System

A robust e-commerce backend system built with Python, featuring secure user authentication, product management, order processing, and more.

## 🌟 Features

### Core Functionality
- **User Management**
  - Customer registration and authentication
  - Role-based access control (Admin/Customer)
  - Secure password hashing with bcrypt

- **Product Management**
  - View all available products
  - Real-time stock tracking
  - Admin-only product addition
  - Product purchase system

- **Shopping Features**
  - View product details (name, price, stock)
  - Purchase products with quantity selection
  - Automatic stock updates after purchase
  - Purchase confirmation system

### Security Features
- Password hashing using bcrypt
- Role-based access control
- Secure database transactions
- Input validation and sanitization
- Protected admin functionalities
- Session management

### Database Security & Privacy
- **Data Encryption**
  - Fernet encryption for sensitive data
  - Secure key generation
  - Encrypted data storage and retrieval

- **Access Control**
  - Exclusive database connections
  - Connection timeouts
  - Foreign key constraints
  - PRAGMA secure settings

- **Security Monitoring**
  - Security audit logging
  - User action tracking
  - IP address monitoring
  - Timestamp tracking

- **SQL Injection Protection**
  - Query parameterization
  - Pattern detection
  - Security exception handling

- **Enhanced User Security**
  - Failed login attempt tracking
  - Account locking mechanism
  - Last login monitoring
  - Creation time tracking

### Encryption Implementation Details
The system implements Fernet symmetric encryption from the cryptography library for data protection.

#### 1. Key Generation
```python
def _generate_key(self):
    """Generate a secure encryption key"""
    key = os.urandom(32)
    return b64encode(key)
```
Generates a secure 32-byte random key using Python's cryptographically secure random number generator.

#### 2. Data Encryption
```python
def _encrypt_data(self, data):
    """Encrypt sensitive data before storing"""
    if isinstance(data, str):
        return self.fernet.encrypt(data.encode()).decode()
    return data
```
Used to encrypt sensitive information before database storage.

#### 3. Data Decryption
```python
def _decrypt_data(self, data):
    """Decrypt data when retrieving"""
    if isinstance(data, str):
        try:
            return self.fernet.decrypt(data.encode()).decode()
        except:
            return data
    return data
```
Securely decrypts data when retrieved from the database.

#### 4. Implementation Example
```python
def execute_query(self, query, params=None):
    if params:
        # Encrypt sensitive parameters
        encrypted_params = [
            self._encrypt_data(p) if isinstance(p, str) else p 
            for p in params
        ]
        cursor.execute(query, encrypted_params)
```
Automatically encrypts string parameters in database queries.

### Object-Oriented Design Principles
- **Encapsulation**
  - Private data members
  - Getter/setter methods
  - Protected class attributes

- **Inheritance**
  - Base user class
  - Admin/Customer specialized classes
  - Reusable code structure

- **Polymorphism**
  - Method overriding
  - Interface implementation
  - Dynamic method dispatch

- **Abstraction**
  - Clear class interfaces
  - Hidden implementation details
  - Modular design

### Database Structure
- Customers
  - User credentials
  - Role information
  - Personal details

- Products
  - Product information
  - Pricing details
  - Stock quantities

- Stock Management
  - Real-time tracking
  - Automatic updates
  - Purchase history

---

## 🚀 Getting Started

### Prerequisites
```bash
# Required Python version
Python 3.8+

# Required packages
pip install -r requirements.txt
```

### Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/online-shopping-system.git
cd online-shopping-system
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the system
```bash
python test_data.py
```

---

## 📁 Project Structure
```
online-shopping-system/
├── main.py           # Main application logic and OnlineShoppingSystem class
├── test_data.py      # Interactive menu system and test data
└── requirements.txt   # Project dependencies
```

---

## 🔧 Core Components

### 1. Main System (main.py)
- User registration and authentication
- Product management
- Stock control
- Security implementations
- OOP structure

### 2. Interactive Menu (test_data.py)
- User registration and login
- Product viewing and purchase
- Admin product management
- Stock tracking
- Secure transactions

---

## 📝 Usage Examples

### For Users
1. Register new account or login
2. View available products
3. Select products to purchase
4. Confirm purchases
5. View updated stock levels

### For Administrators
1. Login with admin credentials
2. Add new products to the system
3. View all products and stock levels
4. Manage product inventory

---

## 👥 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📧 Contact
Mohammed Harahsheh - mohmmedh1@hotmail.com


