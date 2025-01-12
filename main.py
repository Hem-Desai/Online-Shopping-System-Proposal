from database import DatabaseConnection
from security import SecurityManager
from models import Customer, Product, Order, CustomerRepository, ProductRepository, PaymentRepository, DeliveryRepository, Payment, Delivery
import logging
from decimal import Decimal
import bcrypt
import sqlite3
import hashlib
import os
from cryptography.fernet import Fernet
from base64 import b64encode

class OnlineShoppingSystem:
    """Main class for the Online Shopping System."""
    
    def __init__(self):
        """Initialize the system with necessary components."""
        # Setup logging first
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        try:
            self.db = DatabaseConnection()
            self.security = SecurityManager()
            self.customer_repo = CustomerRepository(self.db, self.security)
            self.product_repo = ProductRepository(self.db)
            self.payment_repo = PaymentRepository(self.db)
            self.delivery_repo = DeliveryRepository(self.db)
            self.current_user = None
        except Exception as e:
            self.logger.error(f"Failed to initialize system: {str(e)}")
            raise
    
    def register_user(self, name: str, email: str, password: str, is_admin: bool = False) -> bool:
        """Register a new user."""
        try:
            # Hash the password before storing
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            with self.db.get_connection() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO customers (name, email, password_hash, is_admin)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, email, hashed_password, is_admin)
                )
                return True
        except Exception as e:
            self.logger.error(f"Error registering user: {str(e)}")
            return False
    
    def login(self, email: str, password: str) -> bool:
        """Log in a user."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute(
                    """SELECT customer_id, name, email, password_hash, is_admin 
                    FROM customers WHERE email = ?""",
                    (email,)
                )
                user_data = cursor.fetchone()
                
                if user_data and bcrypt.checkpw(
                    password.encode('utf-8'),
                    user_data[3]  # password_hash
                ):
                    # Set the current user after successful login
                    self.current_user = Customer(
                        customer_id=user_data[0],
                        name=user_data[1],
                        email=user_data[2],
                        password_hash=user_data[3],
                        is_admin=user_data[4]
                    )
                    return True
                return False
        except Exception as e:
            self.logger.error(f"Error during login: {str(e)}")
            return False
    
    def add_product(self, name: str, price: float, quantity: int, description: str = None) -> bool:
        """Add a new product (admin only)."""
        if not self.current_user:
            self.logger.warning("No user logged in")
            return False
            
        if not self.current_user.is_admin:
            self.logger.warning("Unauthorized attempt to add product")
            return False
            
        try:
            product = Product(
                name=name,
                price=Decimal(str(price)),
                stock_quantity=quantity,
                description=description
            )
            created_product = self.product_repo.create_product(product)
            
            if created_product:
                self.logger.info(f"Product {name} added successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error adding product: {str(e)}")
            return False
    
    def process_order(self, order: Order) -> bool:
        """Process a complete order including payment and delivery setup"""
        try:
            # Create payment
            payment = Payment(order_id=order.order_id, amount=order.total_amount)
            if not self.payment_repo.process_payment(payment):
                return False

            # Initialize delivery
            delivery = Delivery(order_id=order.order_id)
            if not self.delivery_repo.update_delivery_status(delivery.delivery_id, "pending"):
                return False

            return True
        except Exception as e:
            self.logger.error(f"Order processing error: {str(e)}")
            return False

class DatabaseManager:
    def __init__(self, db_path):
        # Generate a secure key for database encryption
        self.key = self._generate_key()
        self.fernet = Fernet(self.key)
        self.db_path = db_path
        
        # Set up logging for security events
        logging.basicConfig(
            filename='security.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Set up database with encryption
        self._setup_database()

    def _generate_key(self):
        """Generate a secure encryption key"""
        key = os.urandom(32)
        return b64encode(key)

    def _encrypt_data(self, data):
        """Encrypt sensitive data before storing"""
        if isinstance(data, str):
            return self.fernet.encrypt(data.encode()).decode()
        return data

    def _decrypt_data(self, data):
        """Decrypt data when retrieving"""
        if isinstance(data, str):
            try:
                return self.fernet.decrypt(data.encode()).decode()
            except:
                return data
        return data

    def get_connection(self):
        """Create a secure database connection with timeout and isolation level"""
        try:
            conn = sqlite3.connect(
                self.db_path, 
                timeout=30,
                isolation_level='EXCLUSIVE'
            )
            # Enable foreign key support
            conn.execute("PRAGMA foreign_keys = ON")
            # Set secure delete
            conn.execute("PRAGMA secure_delete = ON")
            
            # Log successful connection
            logging.info(f"Database connection established from {os.getpid()}")
            
            return conn
        except Exception as e:
            logging.error(f"Database connection failed: {str(e)}")
            raise

    def execute_query(self, query, params=None):
        """Execute a query with security measures"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Log query attempt (excluding sensitive data)
                logging.info(f"Executing query: {query.split()[0]}")
                
                # Check for SQL injection attempts
                if self._check_sql_injection(query):
                    logging.warning(f"Potential SQL injection detected: {query}")
                    raise SecurityException("Potential SQL injection detected")
                
                if params:
                    # Encrypt sensitive parameters
                    encrypted_params = [
                        self._encrypt_data(p) if isinstance(p, str) else p 
                        for p in params
                    ]
                    cursor.execute(query, encrypted_params)
                else:
                    cursor.execute(query)
                
                conn.commit()
                return cursor

        except Exception as e:
            logging.error(f"Query execution failed: {str(e)}")
            raise

    def _check_sql_injection(self, query):
        """Check for common SQL injection patterns"""
        suspicious_patterns = [
            "DROP TABLE",
            "DELETE FROM",
            "INSERT INTO",
            "UPDATE",
            ";",
            "UNION",
            "OR '1'='1",
            "OR 1=1"
        ]
        
        query_upper = query.upper()
        return any(pattern.upper() in query_upper for pattern in suspicious_patterns)

    def _setup_database(self):
        """Set up database with security measures"""
        try:
            with self.get_connection() as conn:
                # Create users table with encrypted fields
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS customers (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        is_admin BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        failed_attempts INTEGER DEFAULT 0,
                        account_locked BOOLEAN DEFAULT FALSE
                    )
                """)
                
                # Create products table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS products (
                        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price DECIMAL(10,2) NOT NULL,
                        stock_quantity INTEGER NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create security audit log table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS security_audit_log (
                        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_id INTEGER,
                        action TEXT,
                        ip_address TEXT,
                        status TEXT,
                        FOREIGN KEY (user_id) REFERENCES customers(user_id)
                    )
                """)
                
                logging.info("Database tables created successfully")
                
        except Exception as e:
            logging.error(f"Database setup failed: {str(e)}")
            raise

class SecurityException(Exception):
    """Custom exception for security-related issues"""
    pass

# Make the class available for import
__all__ = ['OnlineShoppingSystem']
