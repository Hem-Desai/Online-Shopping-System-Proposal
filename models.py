from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
import logging

@dataclass
class Customer:
    name: str
    email: str
    password_hash: str
    customer_id: Optional[int] = None
    created_at: datetime = datetime.now()
    is_admin: bool = False

    def register(self) -> bool:
        """Register a new customer"""
        pass

    def login(self) -> bool:
        """Login customer"""
        pass

    def place_order(self, products: List['Product']) -> Optional['Order']:
        """Place a new order"""
        pass

@dataclass
class Product:
    name: str
    price: Decimal
    stock_quantity: int
    product_id: Optional[int] = None
    description: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def update_stock(self, quantity: int) -> bool:
        """Update product stock quantity"""
        pass

    def add_product(self) -> bool:
        """Add new product to inventory"""
        pass

    def delete_product(self) -> bool:
        """Remove product from inventory"""
        pass

@dataclass
class Order:
    customer_id: int
    total_amount: Decimal
    status: str
    order_id: Optional[int] = None
    order_date: datetime = datetime.now()
    items: List['OrderItem'] = None

    def calculate_total(self) -> Decimal:
        """Calculate total amount of order"""
        return sum(item.price_at_time * item.quantity for item in self.items) if self.items else Decimal('0')

    def track_status(self) -> str:
        """Track current order status"""
        return self.status

@dataclass
class OrderItem:
    product_id: int
    quantity: int
    price_at_time: Decimal
    order_item_id: Optional[int] = None
    order_id: Optional[int] = None

@dataclass
class Payment:
    order_id: int
    amount: Decimal
    payment_id: Optional[int] = None
    payment_date: datetime = datetime.now()
    status: str = 'pending'

    def process_payment(self) -> bool:
        """Process the payment"""
        pass

    def refund_payment(self) -> bool:
        """Process a refund"""
        pass

@dataclass
class Delivery:
    order_id: int
    delivery_id: Optional[int] = None
    delivery_status: str = 'pending'
    delivery_date: Optional[datetime] = None

    def update_status(self, status: str) -> bool:
        """Update delivery status"""
        pass

    def confirm_delivery(self) -> bool:
        """Confirm delivery completion"""
        pass

class CustomerRepository:
    """Handles database operations for Customer entities."""
    
    def __init__(self, db_connection, security_manager):
        self.db = db_connection
        self.security = security_manager
        self.logger = logging.getLogger(__name__)
    
    def create_customer(self, customer: Customer) -> Optional[Customer]:
        """Create a new customer in the database."""
        query = """
            INSERT INTO customers (name, email, password_hash, is_admin)
            VALUES (?, ?, ?, ?)
        """
        try:
            cursor = self.db.execute_query(
                query,
                (customer.name, customer.email, customer.password_hash, customer.is_admin)
            )
            customer.customer_id = cursor.lastrowid
            return customer
        except Exception as e:
            self.logger.error(f"Error creating customer: {str(e)}")
            return None
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Retrieve a customer by email."""
        query = """
            SELECT customer_id, name, password_hash, email, created_at, is_admin 
            FROM customers WHERE email = ?
        """
        try:
            result = self.db.fetch_all(query, (email,))
            if result and len(result) > 0:
                row = result[0]
                return Customer(
                    name=row[1],
                    email=row[3],
                    password_hash=row[2],
                    customer_id=row[0],
                    created_at=datetime.fromisoformat(row[4]),
                    is_admin=bool(row[5])
                )
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving customer: {str(e)}")
            return None

class ProductRepository:
    """Handles database operations for Product entities."""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.logger = logging.getLogger(__name__)
    
    def create_product(self, product: Product) -> Optional[Product]:
        """Create a new product in the database."""
        query = """
            INSERT INTO products (name, price, stock_quantity, description)
            VALUES (?, ?, ?, ?)
        """
        try:
            cursor = self.db.execute_query(
                query,
                (
                    product.name,
                    str(product.price),
                    product.stock_quantity,
                    product.description
                )
            )
            product.product_id = cursor.lastrowid
            return product
        except Exception as e:
            self.logger.error(f"Error creating product: {str(e)}")
            return None

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Retrieve a product by ID."""
        query = """
            SELECT product_id, name, price, stock_quantity, description, created_at, updated_at
            FROM products WHERE product_id = ?
        """
        try:
            result = self.db.execute_query(query, (product_id,))
            if result and len(result) > 0:
                row = result[0]
                return Product(
                    product_id=row[0],
                    name=row[1],
                    price=Decimal(str(row[2])),
                    stock_quantity=row[3],
                    description=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                    updated_at=datetime.fromisoformat(row[6])
                )
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving product: {str(e)}")
            return None

class PaymentRepository:
    """Handles database operations for Payment entities."""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.logger = logging.getLogger(__name__)
    
    def process_payment(self, payment: Payment) -> bool:
        """Process a payment in the database."""
        query = """
            INSERT INTO payments (order_id, amount, status)
            VALUES (?, ?, ?)
        """
        try:
            self.db.execute_query(query, (payment.order_id, payment.amount, payment.status))
            return True
        except Exception as e:
            self.logger.error(f"Error processing payment: {str(e)}")
            return False

class DeliveryRepository:
    """Handles database operations for Delivery entities."""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.logger = logging.getLogger(__name__)
    
    def update_delivery_status(self, delivery_id: int, status: str) -> bool:
        """Update delivery status in the database."""
        query = """
            UPDATE deliveries 
            SET delivery_status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE delivery_id = ?
        """
        try:
            self.db.execute_query(query, (status, delivery_id))
            return True
        except Exception as e:
            self.logger.error(f"Error updating delivery status: {str(e)}")
            return False

# ... Rest of repository classes (ProductRepository, OrderRepository, etc.) ...