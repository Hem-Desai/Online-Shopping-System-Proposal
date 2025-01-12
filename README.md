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


