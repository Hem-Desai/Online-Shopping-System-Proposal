import sqlite3
from typing import Optional
from contextlib import contextmanager
import logging

class DatabaseConnection:
    """Manages database connections and setup for the Online Shopping System."""
    
    def __init__(self, db_name: str = "shop.db"):
        self.db_name = db_name
        self.setup_logging()
        self.initialize_database()
    
    def setup_logging(self):
        """Configure logging for database operations."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            conn.execute("PRAGMA foreign_keys = ON")
            yield conn
            conn.commit()
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def initialize_database(self):
        """Create database tables if they don't exist."""
        try:
            with self.get_connection() as conn:
                # Customers table (changed from users)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS customers (
                        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_admin BOOLEAN DEFAULT 0
                    )
                """)
                
                # Products table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS products (
                        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        price DECIMAL(10,2) NOT NULL,
                        stock_quantity INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Orders table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id INTEGER NOT NULL,
                        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status TEXT NOT NULL,
                        total_amount DECIMAL(10,2) NOT NULL,
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                    )
                """)
                
                # Order items table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS order_items (
                        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        price_at_time DECIMAL(10,2) NOT NULL,
                        FOREIGN KEY (order_id) REFERENCES orders(order_id),
                        FOREIGN KEY (product_id) REFERENCES products(product_id)
                    )
                """)

                # Payments table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS payments (
                        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id INTEGER NOT NULL,
                        amount DECIMAL(10,2) NOT NULL,
                        status TEXT NOT NULL,
                        payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (order_id) REFERENCES orders(order_id)
                    )
                """)

                # Deliveries table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS deliveries (
                        delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id INTEGER NOT NULL,
                        delivery_status TEXT NOT NULL,
                        delivery_date TIMESTAMP,
                        FOREIGN KEY (order_id) REFERENCES orders(order_id)
                    )
                """)
                
                self.logger.info("Database initialized successfully")
                
        except sqlite3.Error as e:
            self.logger.error(f"Error initializing database: {str(e)}")
            raise

    def execute_query(self, query: str, parameters: tuple = ()) -> Optional[sqlite3.Cursor]:
        """Execute a SQL query with parameters."""
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            connection.row_factory = sqlite3.Row
            cursor = connection.execute(query, parameters)
            connection.commit()
            return cursor  # Return the cursor instead of fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"Query execution error: {str(e)}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()

    def fetch_all(self, query: str, parameters: tuple = ()):
        """Execute a query and fetch all results."""
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            connection.row_factory = sqlite3.Row
            cursor = connection.execute(query, parameters)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            self.logger.error(f"Query execution error: {str(e)}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()