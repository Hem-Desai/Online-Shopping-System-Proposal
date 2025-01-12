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
├── main.py              # Main application logic and OnlineShoppingSystem class
├── test_data.py         # Interactive menu system and test data
├── security/
│   ├── __init__.py
│   ├── privacy.py       # DataPrivacyManager implementation
│   ├── database.py      # SecureDatabase implementation
│   ├── access.py        # DataAccessControl implementation
│   └── operations.py    # SecureDataOperations implementation
├── utils/
│   ├── __init__.py
│   └── logging.py       # Audit logging utilities
├── encryption.key       # Encrypted key storage (generated on first run)
└── requirements.txt     # Project dependencies
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

### Database Security & Privacy Implementation

#### 1. Data Privacy Manager
Handles encryption and secure storage of sensitive data using Fernet symmetric encryption.

```python
from cryptography.fernet import Fernet
import base64
import os

class DataPrivacyManager:
    def __init__(self):
        self.encryption_key = self._load_or_generate_key()
        self.fernet = Fernet(self.encryption_key)
        
    def _load_or_generate_key(self):
        """Load existing key or generate new one"""
        key_file = "encryption.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key
            
    def encrypt_personal_data(self, data):
        """Encrypt personal information"""
        if isinstance(data, str):
            return self.fernet.encrypt(data.encode()).decode()
        return data
        
    def decrypt_personal_data(self, encrypted_data):
        """Decrypt personal information"""
        if isinstance(encrypted_data, str):
            try:
                return self.fernet.decrypt(encrypted_data.encode()).decode()
            except:
                return encrypted_data
        return encrypted_data
```

#### 2. Enhanced Database Security
Provides thread-safe database connections with security features and audit logging.

```python
import sqlite3
from contextlib import contextmanager
import threading

class SecureDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection_pool = {}
        self._setup_database()
        
    def _setup_database(self):
        """Initialize database with security settings"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Enable security features
            cursor.executescript("""
                PRAGMA foreign_keys = ON;
                PRAGMA secure_delete = ON;
                PRAGMA journal_mode = WAL;
                PRAGMA synchronous = NORMAL;
                PRAGMA temp_store = MEMORY;
                PRAGMA mmap_size = 30000000000;
            """)
            
            # Create audit log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER,
                    action TEXT,
                    table_name TEXT,
                    record_id INTEGER,
                    old_value TEXT,
                    new_value TEXT
                )
            """)

    @contextmanager
    def get_connection(self):
        """Get thread-safe database connection"""
        thread_id = threading.get_ident()
        if thread_id not in self.connection_pool:
            self.connection_pool[thread_id] = sqlite3.connect(
                self.db_name,
                timeout=30,
                isolation_level='EXCLUSIVE'
            )
        try:
            yield self.connection_pool[thread_id]
        finally:
            if thread_id in self.connection_pool:
                self.connection_pool[thread_id].close()
                del self.connection_pool[thread_id]
```

#### 3. Data Access Control
Implements role-based access control for database operations.

```python
from enum import Enum
from functools import wraps

class AccessLevel(Enum):
    READ = 1
    WRITE = 2
    ADMIN = 3

class DataAccessControl:
    def __init__(self, db):
        self.db = db
        self.user_permissions = {}

    def require_permission(self, required_level):
        """Decorator to check permission level"""
        def decorator(f):
            @wraps(f)
            def wrapped(self, user_id, *args, **kwargs):
                if not self._check_permission(user_id, required_level):
                    raise PermissionError(f"User {user_id} lacks {required_level} permission")
                return f(self, user_id, *args, **kwargs)
            return wrapped
        return decorator

    def _check_permission(self, user_id, required_level):
        """Check if user has required permission level"""
        user_level = self.user_permissions.get(user_id, AccessLevel.READ)
        return user_level.value >= required_level.value
```

#### 4. Secure Data Operations
Manages secure data operations with automatic encryption.

```python
class SecureDataOperations:
    def __init__(self, db, privacy_manager):
        self.db = db
        self.privacy_manager = privacy_manager
        
    def insert_user_data(self, user_data):
        """Securely insert user data"""
        encrypted_data = {
            'name': self.privacy_manager.encrypt_personal_data(user_data['name']),
            'email': self.privacy_manager.encrypt_personal_data(user_data['email']),
            'address': self.privacy_manager.encrypt_personal_data(user_data['address'])
        }
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, email, address)
                VALUES (?, ?, ?)
            """, (encrypted_data['name'], encrypted_data['email'], encrypted_data['address']))
            conn.commit()
            
    def get_user_data(self, user_id):
        """Securely retrieve user data"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, email, address FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'name': self.privacy_manager.decrypt_personal_data(row[0]),
                    'email': self.privacy_manager.decrypt_personal_data(row[1]),
                    'address': self.privacy_manager.decrypt_personal_data(row[2])
                }
            return None
```

Usage Example:
```python
# Initialize components
db = SecureDatabase('shop.db')
privacy_manager = DataPrivacyManager()
data_ops = SecureDataOperations(db, privacy_manager)
access_control = DataAccessControl(db)

# Insert user data
user_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'address': '123 Main St'
}
data_ops.insert_user_data(user_data)

# Retrieve user data
user = data_ops.get_user_data(1)

# Log audit event
db.log_audit_event(
    user_id=1,
    action='INSERT',
    table_name='users',
    record_id=1,
    new_value=str(user_data)
)
```


