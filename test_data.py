from main import OnlineShoppingSystem
from decimal import Decimal
import logging
import time
import os
from getpass import getpass

def setup_test_data():
    """Insert mock data and test basic functionality."""
    shop = OnlineShoppingSystem()
    
    try:
        # Check if database already has users
        with shop.db.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM customers")
            user_count = cursor.fetchone()[0]
            
            if user_count > 0:
                print("\nDatabase already contains users. Skipping test data setup.")
                return True
                
        # If no users exist, create test data
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

def run_interactive_menu():
    shop = OnlineShoppingSystem()
    while True:  # Add main loop
        print("\n=== Main Menu ===")
        print("1. Create new account")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            print("\n=== Create New Account ===")
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = getpass("Enter your password: ")
            
            user_created = shop.register_user(
                name=name,
                email=email,
                password=password,
                is_admin=False
            )
            
            if user_created:
                print("Account created successfully!")
                print("\n=== User Login ===")
                email = input("Enter email: ")
                password = getpass("Enter password: ")
                
                login_success = shop.login(email=email, password=password)
                if login_success:
                    print("Login successful!")
                    show_product_menu(shop)  # Add this line
                    return
                else:
                    print("Login failed. Invalid credentials.")
            else:
                print("Failed to create account. Email might already exist.")
            
        elif choice == "2":
            print("\n=== User Login ===")
            email = input("Enter email: ")
            password = getpass("Enter password: ")
            
            login_success = shop.login(email=email, password=password)
            if login_success:
                print("Login successful!")
                show_product_menu(shop)  # Add this line
                return
            else:
                print("Login failed. Invalid credentials.")
            
        elif choice == "3":
            print("Goodbye!")
            break  # Add break instead of just returning
            
        else:
            print("Invalid choice. Please try again.")

def show_product_menu(shop):
    while True:
        print("\n=== Product Menu ===")
        print("1. View all products")
        print("2. Select product to purchase")
        if shop.current_user and shop.current_user.is_admin:
            print("3. Add new product (Admin only)")
            print("4. Logout")
        else:
            print("3. Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            with shop.db.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT name, price, stock_quantity, description FROM products"
                )
                print("\n=== Available Products ===")
                for row in cursor.fetchall():
                    print(f"Name: {row[0]}")
                    print(f"Price: ${row[1]}")
                    print(f"Stock: {row[2]}")
                    print(f"Description: {row[3]}")
                    print("-" * 30)
                    
        elif choice == "2":
            # Show products with IDs for selection
            with shop.db.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT product_id, name, price, stock_quantity FROM products"
                )
                products = cursor.fetchall()
                
                print("\n=== Select a Product ===")
                for product in products:
                    print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]}, Stock: {product[3]}")
                
                try:
                    product_id = int(input("\nEnter product ID to purchase (0 to cancel): "))
                    if product_id == 0:
                        continue
                    
                    # Get current stock for the selected product
                    cursor = conn.execute(
                        "SELECT stock_quantity, name, price FROM products WHERE product_id = ?",
                        (product_id,)
                    )
                    product = cursor.fetchone()
                    
                    if not product:
                        print("Invalid product ID!")
                        continue
                        
                    current_stock = product[0]
                    product_name = product[1]
                    price = product[2]
                    
                    quantity = int(input("Enter quantity: "))
                    
                    # Check if enough stock
                    if quantity <= 0:
                        print("Please enter a valid quantity!")
                        continue
                    
                    if quantity > current_stock:
                        print(f"Sorry, only {current_stock} items available in stock!")
                        continue
                    
                    # Calculate total price
                    total_price = price * quantity
                    
                    # Confirm purchase
                    print(f"\nOrder Summary:")
                    print(f"Product: {product_name}")
                    print(f"Quantity: {quantity}")
                    print(f"Total Price: ${total_price:.2f}")
                    
                    confirm = input("\nConfirm purchase? (y/n): ").lower()
                    if confirm == 'y':
                        # Update stock quantity
                        new_quantity = current_stock - quantity
                        cursor.execute(
                            "UPDATE products SET stock_quantity = ? WHERE product_id = ?",
                            (new_quantity, product_id)
                        )
                        conn.commit()
                        print("\nPurchase successful! Thank you for your order.")
                        print(f"Remaining stock: {new_quantity}")
                    else:
                        print("Purchase cancelled.")
                    
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    
        elif choice == "3" and shop.current_user and shop.current_user.is_admin:
            print("\n=== Add New Product ===")
            name = input("Enter product name: ")
            price = float(input("Enter price: "))
            quantity = int(input("Enter stock quantity: "))
            description = input("Enter product description: ")
            
            product_added = shop.add_product(
                name=name,
                price=price,
                quantity=quantity,
                description=description
            )
            
            if product_added:
                print("Product added successfully!")
            else:
                print("Failed to add product.")
                
        elif (choice == "4" and shop.current_user and shop.current_user.is_admin) or \
             (choice == "3" and not shop.current_user.is_admin):
            print("Logging out...")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    success = setup_test_data()
    if success:
        print("\nTest data setup completed successfully!")
        run_interactive_menu()
    else:
        print("\nError setting up test data. Check logs for details.")
