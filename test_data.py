from main import OnlineShoppingSystem
from decimal import Decimal
import logging
import time
import os

def setup_test_data():
    """Insert mock data and test basic functionality."""
    # Delete existing database
    if os.path.exists("shop.db"):
        os.remove("shop.db")
        time.sleep(1)  # Add small delay to ensure file is deleted
        
    # Initialize the system
    shop = OnlineShoppingSystem()
    
    try:
        # 1. Create test users (1 admin, 2 regular users)
        print("\n=== Creating Test Users ===")
        
        # Admin user
        admin_created = shop.register_user(
            name="Admin User",
            email="admin@shop.com",
            password="Admin123!",
            is_admin=True
        )
        if not admin_created:
            raise Exception("Failed to create admin user")
        print(f"Admin user created: {admin_created}")
        
        # Regular users
        user1_created = shop.register_user(
            name="John Doe",
            email="john@example.com",
            password="JohnDoe123!"
        )
        if not user1_created:
            raise Exception("Failed to create user1")
            
        user2_created = shop.register_user(
            name="Jane Smith",
            email="jane@example.com",
            password="JaneSmith123!"
        )
        if not user2_created:
            raise Exception("Failed to create user2")
        print(f"Regular users created: {user1_created}, {user2_created}")
        
        # 2. Login as admin to add products
        print("\n=== Testing Admin Login ===")
        admin_login = shop.login(email="admin@shop.com", password="Admin123!")
        if not admin_login:
            raise Exception("Admin login failed")
        print(f"Admin login successful: {admin_login}")
        
        # 3. Add test products
        print("\n=== Adding Test Products ===")
        products = [
            ("Laptop Pro X", 1299.99, 10, "High-performance laptop with 16GB RAM"),
            ("Wireless Mouse", 29.99, 50, "Ergonomic wireless mouse"),
            ("USB-C Cable", 15.99, 100, "1.5m USB-C charging cable"),
            ("Backpack", 49.99, 30, "Water-resistant laptop backpack"),
            ("Screen Protector", 19.99, 200, "Tempered glass screen protector")
        ]
        
        for name, price, quantity, description in products:
            product_added = shop.add_product(
                name=name,
                price=price,
                quantity=quantity,
                description=description
            )
            if not product_added:
                raise Exception(f"Failed to add product: {name}")
            print(f"Product '{name}' added: {product_added}")
        
        # 4. Verify data
        print("\n=== Verifying Data ===")
        
        # Check users
        with shop.db.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM customers")
            user_count = cursor.fetchone()[0]
            print(f"Total users in database: {user_count}")
            
            # Check products
            cursor = conn.execute("SELECT COUNT(*) FROM products")
            product_count = cursor.fetchone()[0]
            print(f"Total products in database: {product_count}")
            
            # Show all products
            print("\n=== Product List ===")
            cursor = conn.execute(
                "SELECT name, price, stock_quantity FROM products"
            )
            for row in cursor.fetchall():
                print(f"Product: {row[0]}, Price: ${row[1]}, Stock: {row[2]}")
        
        return True
        
    except Exception as e:
        logging.error(f"Error in test setup: {str(e)}")
        return False

if __name__ == "__main__":
    success = setup_test_data()
    if success:
        print("\nTest data setup completed successfully!")
    else:
        print("\nError setting up test data. Check logs for details.")
