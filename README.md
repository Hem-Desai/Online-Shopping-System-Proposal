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

### Security Implementation Examples

#### 1. Enhanced Encryption System
```python
from cryptography.fernet import Fernet
from base64 import b64encode
import os

class SecurityManager:
    def __init__(self):
        self.key = self._generate_key()
        self.fernet = Fernet(self.key)
        self.max_login_attempts = 3
        self.lockout_time = 300  # 5 minutes

    def _generate_key(self):
        """Generate a secure encryption key"""
        return Fernet.generate_key()

    def encrypt_sensitive_data(self, data):
        """Encrypt sensitive data using Fernet"""
        if not isinstance(data, bytes):
            data = str(data).encode()
        return self.fernet.encrypt(data)

    def decrypt_sensitive_data(self, encrypted_data):
        """Decrypt Fernet-encrypted data"""
        try:
            return self.fernet.decrypt(encrypted_data)
        except Exception as e:
            logging.error(f"Decryption failed: {e}")
            raise SecurityException("Failed to decrypt data")
```

**Description:**
The SecurityManager implements enterprise-grade encryption using Fernet symmetric encryption:
- Uses AES-128 in CBC mode with PKCS7 padding
- Generates cryptographically secure keys using `os.urandom()`
- Handles automatic encoding/decoding of data
- Includes comprehensive error handling and logging

Key Features:
- Automatic key management
- Secure data transformation
- Error recovery
- Memory security

Usage Example:
```python
# Initialize security manager
security = SecurityManager()

# Encrypt sensitive data
encrypted = security.encrypt_sensitive_data("sensitive_info")

# Decrypt when needed
decrypted = security.decrypt_sensitive_data(encrypted)
```

#### 2. Database Security Implementation
```python
class DatabaseManager:
    def __init__(self):
        self.connection = None
        self._setup_database()

    def _setup_database(self):
        """Setup secure database connection with proper PRAGMA settings"""
        self.connection = sqlite3.connect('shop.db', timeout=30)
        cursor = self.connection.cursor()
        
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Set secure delete
        cursor.execute("PRAGMA secure_delete = ON")
        
        # Enable WAL mode for better concurrency
        cursor.execute("PRAGMA journal_mode = WAL")

    def create_connection(self):
        """Create a new database connection with timeout"""
        try:
            return sqlite3.connect('shop.db', timeout=30)
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            raise DatabaseException("Failed to establish database connection")
```

**Description:**
The DatabaseManager ensures secure database operations through:
- Connection timeouts to prevent DOS attacks
- Foreign key constraints for data integrity
- Secure delete operations
- Write-Ahead Logging for safe concurrent access

Implementation Features:
- 30-second connection timeout
- Automatic connection recovery
- Transaction safety
- Resource cleanup

Usage Example:
```python
# Initialize database manager
db = DatabaseManager()

# Create new connection
connection = db.create_connection()
```

#### 3. SQL Injection Protection
```python
class QueryManager:
    def __init__(self, db_connection):
        self.connection = db_connection

    def execute_safe_query(self, query, params=None):
        """Execute parameterized queries to prevent SQL injection"""
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except sqlite3.Error as e:
            self.connection.rollback()
            logging.error(f"Query execution failed: {e}")
            raise DatabaseException("Query execution failed")

    def select_user(self, username):
        """Example of safe user selection"""
        query = "SELECT * FROM users WHERE username = ?"
        return self.execute_safe_query(query, (username,))
```

**Description:**
The QueryManager prevents SQL injection through:
- Parameterized queries
- Input validation
- Transaction management
- Error handling

Security Measures:
- No string concatenation
- Parameter sanitization
- Transaction rollback on errors
- Query logging

Usage Example:
```python
# Initialize query manager
query_mgr = QueryManager(db_connection)

# Execute safe query
result = query_mgr.select_user("john_doe")
```

#### 4. User Authentication and Session Management
```python
class AuthenticationManager:
    def __init__(self):
        self.security = SecurityManager()
        self.failed_attempts = {}
        self.sessions = {}

    def authenticate_user(self, username, password):
        """Secure user authentication with rate limiting"""
        if self._is_account_locked(username):
            raise SecurityException("Account is temporarily locked")

        user = self.get_user(username)
        if not user:
            self._record_failed_attempt(username)
            raise AuthenticationException("Invalid credentials")

        if not self._verify_password(password, user['password_hash']):
            self._record_failed_attempt(username)
            raise AuthenticationException("Invalid credentials")

        self._clear_failed_attempts(username)
        return self._create_session(user)

    def _is_account_locked(self, username):
        """Check if account is locked due to too many failed attempts"""
        if username in self.failed_attempts:
            attempts = self.failed_attempts[username]
            if attempts['count'] >= 3:
                lock_time = attempts['last_attempt'] + timedelta(minutes=5)
                if datetime.now() < lock_time:
                    return True
        return False
```

**Description:**
The AuthenticationManager provides:
- Rate limiting for login attempts
- Account lockout mechanism
- Secure password verification
- Session management

Security Features:
- 3-attempt limit before lockout
- 5-minute lockout duration
- Secure session handling
- Failed attempt tracking

Usage Example:
```python
# Initialize authentication manager
auth_mgr = AuthenticationManager()

# Attempt login
try:
    session = auth_mgr.authenticate_user("username", "password")
except SecurityException as e:
    print("Account locked:", e)
```

#### 5. Security Audit Logging
```python
class AuditLogger:
    def __init__(self):
        self.log_file = "security_audit.log"
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def log_security_event(self, event_type, user, ip_address, details):
        """Log security-related events"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user': user,
            'ip_address': ip_address,
            'details': details
        }
        logging.info(json.dumps(log_entry))

    def log_failed_login(self, username, ip_address):
        """Log failed login attempts"""
        self.log_security_event(
            'FAILED_LOGIN',
            username,
            ip_address,
            'Failed login attempt'
        )
```

**Description:**
The AuditLogger provides comprehensive security monitoring:
- Timestamped event logging
- JSON-formatted log entries
- IP address tracking
- Event categorization

Logging Features:
- Automatic timestamp generation
- Structured log format
- Multiple event types
- Easy log analysis

Usage Example:
```python
# Initialize audit logger
audit = AuditLogger()

# Log security event
audit.log_failed_login("username", "192.168.1.1")
```

### Implementation Best Practices

1. **Encryption:**
   - Store keys securely
   - Rotate keys regularly
   - Use environment variables
   - Implement key backup

2. **Database:**
   - Regular backups
   - Connection pooling
   - Timeout management
   - Error monitoring

3. **SQL Protection:**
   - Always use parameters
   - Validate all inputs
   - Implement timeouts
   - Monitor queries

4. **Authentication:**
   - Strong password rules
   - Session timeouts
   - Regular cleanup
   - Activity monitoring

5. **Logging:**
   - Regular rotation
   - Secure storage
   - Analysis tools
   - Retention policies


