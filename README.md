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
  - Fernet encryption for sensitive data
  - Secure key generation
  - Encrypted data storage and retrieval

- **Access Control**
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
  - Exclusive database connections
  - Connection timeouts
  - Foreign key constraints
  - PRAGMA secure settings

- **Security Monitoring**
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
  - Security audit logging
  - User action tracking
  - IP address monitoring
  - Timestamp tracking

- **SQL Injection Protection**
```python
from typing import Any, List, Dict
import re

class SQLInjectionProtection:
    def __init__(self):
        self.sql_patterns = [
            r'(\s*([\0\b\'\"\n\r\t\%\_\\]*\s*(((select\s*.+\s*from)|(insert\s*.+\s*into)|(update\s*.+\s*set)|(delete\s*.+\s*from)|(drop\s*.+)|(truncate\s*.+)|(alter\s*.+)|(exec\s*.+)|(\s*(all|any|not|and|between|in|like|or|some|contains|containsall|containskey)\s*.+[\=\>\<=\!\~]+))\s*[\"\s\'\/\*]+)))',
            r'((\%27)|(\'))\s*((\%6F)|o|(\%4F))((\%72)|r|(\%52))',
            r'((\%27)|(\'))\s*((\%6F)|o|(\%4F))((\%72)|r|(\%52))',
            r'((\%27)|(\'))\s*((\%6F)|o|(\%4F))((\%72)|r|(\%52))'
        ]
        self.prepared_statements = {}
        
    def sanitize_input(self, value: Any) -> Any:
        """Sanitize input to prevent SQL injection"""
        if isinstance(value, str):
            # Remove dangerous SQL characters
            value = re.sub(r'[\0\b\'\"\n\r\t\%\_\\]', '', value)
            # Check for SQL injection patterns
            for pattern in self.sql_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    raise ValueError("Potential SQL injection detected")
        return value

    def prepare_statement(self, query: str, params: Dict[str, Any] = None) -> tuple:
        """Prepare SQL statement with parameters"""
        if params:
            sanitized_params = {
                key: self.sanitize_input(value)
                for key, value in params.items()
            }
            return (query, sanitized_params)
        return (query, None)

    def execute_safe_query(self, cursor, query: str, params: Dict[str, Any] = None):
        """Execute query with SQL injection protection"""
        try:
            prepared_query, sanitized_params = self.prepare_statement(query, params)
            if sanitized_params:
                cursor.execute(prepared_query, sanitized_params)
            else:
                cursor.execute(prepared_query)
        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            raise DatabaseException("Query execution failed")
```
  - Query parameterization
  - Pattern detection
  - Security exception handling

- **Enhanced User Security**
```python
from datetime import datetime, timedelta
import bcrypt
import jwt

class UserSecurity:
    def __init__(self):
        self.max_attempts = 3
        self.lockout_time = 15  # minutes
        self.attempts = {}
        self.secret = os.urandom(32)

    def check_attempts(self, username):
        """Check if account is locked"""
        if username in self.attempts:
            if self.attempts[username]['count'] >= self.max_attempts:
                if datetime.now() - self.attempts[username]['time'] < timedelta(minutes=self.lockout_time):
                    return False
                self.attempts.pop(username)
        return True

    def track_login(self, username, success):
        """Track login attempts"""
        if success:
            self.attempts.pop(username, None)
        else:
            self.attempts[username] = {
                'count': self.attempts.get(username, {}).get('count', 0) + 1,
                'time': datetime.now()
            }

    def verify_password(self, password, hashed):
        """Verify password"""
        return bcrypt.checkpw(password.encode(), hashed)

    def create_token(self, user_id):
        """Create session token"""
        return jwt.encode(
            {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(hours=24)},
            self.secret,
            algorithm='HS256'
        )
```
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
