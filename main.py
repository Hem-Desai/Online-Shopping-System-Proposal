from database import DatabaseConnection
from security import SecurityManager
from models import Customer, Product, Order, CustomerRepository, ProductRepository, PaymentRepository, DeliveryRepository, Payment, Delivery
import logging
from decimal import Decimal

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
            # Check if user already exists
            if self.customer_repo.get_customer_by_email(email):
                self.logger.warning(f"Email {email} already exists")
                return False
            
            # Hash password and create user
            password_hash = self.security.hash_password(password)
            customer = Customer(name=name, email=email, password_hash=password_hash, is_admin=is_admin)
            created_customer = self.customer_repo.create_customer(customer)
            
            if created_customer:
                self.logger.info(f"User {name} registered successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error registering user: {str(e)}")
            return False
    
    def login(self, email: str, password: str) -> bool:
        """Log in a user."""
        try:
            customer = self.customer_repo.get_customer_by_email(email)
            if not customer:
                self.logger.warning(f"User with email {email} not found")
                return False
            
            if self.security.verify_password(password, customer.password_hash):
                self.current_user = customer
                self.logger.info(f"User {email} logged in successfully")
                return True
            
            self.logger.warning(f"Invalid password for email {email}")
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

# Make the class available for import
__all__ = ['OnlineShoppingSystem']
