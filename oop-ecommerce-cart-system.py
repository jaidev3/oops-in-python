class Product:
    # Class variable to track all products and categories
    all_products = []
    category_stats = {}
    
    def __init__(self, product_id, name, price, category, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity
        
        # Add to class tracking
        Product.all_products.append(self)
        if category in Product.category_stats:
            Product.category_stats[category] += 1
        else:
            Product.category_stats[category] = 1
    
    def get_product_info(self):
        return f"ID: {self.product_id}, Name: {self.name}, Price: ${self.price}, Category: {self.category}, Stock: {self.stock_quantity}"
    
    def update_stock(self, quantity_change):
        """Update stock quantity (positive to add, negative to remove)"""
        self.stock_quantity += quantity_change
        if self.stock_quantity < 0:
            self.stock_quantity = 0
    
    def is_available(self, quantity=1):
        """Check if requested quantity is available"""
        return self.stock_quantity >= quantity
    
    @classmethod
    def get_total_products(cls):
        return len(cls.all_products)
    
    @classmethod
    def get_most_popular_category(cls):
        if not cls.category_stats:
            return None
        return max(cls.category_stats, key=cls.category_stats.get)


class Customer:
    # Class variable to track total revenue across all customers
    total_revenue = 0
    
    def __init__(self, customer_id, name, email, membership_type="standard"):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.membership_type = membership_type
        self.purchase_history = []
        self.total_spent = 0
    
    def get_discount_rate(self):
        """Return discount rate based on membership type"""
        discount_rates = {
            "standard": 0.0,
            "premium": 0.1,  # 10% discount
            "vip": 0.15      # 15% discount
        }
        return discount_rates.get(self.membership_type, 0.0)
    
    def add_purchase(self, amount):
        """Add a purchase to customer's history"""
        self.purchase_history.append(amount)
        self.total_spent += amount
        Customer.total_revenue += amount
    
    @classmethod
    def get_total_revenue(cls):
        return cls.total_revenue


class ShoppingCart:
    def __init__(self, customer):
        self.customer = customer
        self.items = {}  # {product: quantity}
    
    def add_item(self, product, quantity):
        """Add item to cart if stock is available"""
        if product.is_available(quantity):
            if product in self.items:
                self.items[product] += quantity
            else:
                self.items[product] = quantity
            return True
        return False
    
    def remove_item(self, product_id):
        """Remove item from cart by product ID"""
        for product in list(self.items.keys()):
            if product.product_id == product_id:
                del self.items[product]
                return True
        return False
    
    def get_total_items(self):
        """Get total number of items in cart"""
        return sum(self.items.values())
    
    def get_subtotal(self):
        """Calculate subtotal before discount"""
        subtotal = 0
        for product, quantity in self.items.items():
            subtotal += product.price * quantity
        return subtotal
    
    def calculate_total(self):
        """Calculate final total with discount applied"""
        subtotal = self.get_subtotal()
        discount_rate = self.customer.get_discount_rate()
        discount_amount = subtotal * discount_rate
        return subtotal - discount_amount
    
    def place_order(self):
        """Place order and update inventory"""
        if not self.items:
            return "Cart is empty"
        
        # Check if all items are still available
        for product, quantity in self.items.items():
            if not product.is_available(quantity):
                return f"Insufficient stock for {product.name}"
        
        # Calculate total and process order
        total = self.calculate_total()
        
        # Update inventory
        for product, quantity in self.items.items():
            product.update_stock(-quantity)
        
        # Add to customer's purchase history
        self.customer.add_purchase(total)
        
        # Clear cart
        order_summary = f"Order placed successfully! Total: ${total:.2f}"
        self.items.clear()
        
        return order_summary
    
    def get_cart_items(self):
        """Get list of items in cart with details"""
        cart_items = []
        for product, quantity in self.items.items():
            cart_items.append({
                'product': product.name,
                'quantity': quantity,
                'price': product.price,
                'subtotal': product.price * quantity
            })
        return cart_items
    
    def clear_cart(self):
        """Clear all items from cart"""
        self.items.clear()


# Test Case 1: Creating products with different categories
laptop = Product("P001", "Gaming Laptop", 1299.99, "Electronics", 10)
book = Product("P002", "Python Programming", 49.99, "Books", 25)
shirt = Product("P003", "Cotton T-Shirt", 19.99, "Clothing", 50)

print(f"Product info: {laptop.get_product_info()}")
print(f"Total products in system: {Product.get_total_products()}")

# Test Case 2: Creating customer and shopping cart
customer = Customer("C001", "John Doe", "john@email.com", "premium")
cart = ShoppingCart(customer)

print(f"Customer: {customer.name}")
print(f"Customer discount: {customer.get_discount_rate()*100}%")

# Test Case 3: Adding items to cart
cart.add_item(laptop, 1)
cart.add_item(book, 2)
cart.add_item(shirt, 3)

print(f"Cart total items: {cart.get_total_items()}")
print(f"Cart subtotal: ${cart.get_subtotal()}")

# Test Case 4: Applying discounts and calculating final price
final_total = cart.calculate_total()
print(f"Final total (with {customer.get_discount_rate()*100}% discount): ${final_total}")

# Test Case 5: Inventory management
print(f"Laptop stock before order: {laptop.stock_quantity}")
order_result = cart.place_order()
print(f"Order result: {order_result}")
print(f"Laptop stock after order: {laptop.stock_quantity}")

# Test Case 6: Class methods for business analytics
popular_category = Product.get_most_popular_category()
print(f"Most popular category: {popular_category}")

total_revenue = Customer.get_total_revenue()
print(f"Total revenue: ${total_revenue}")

# Test Case 7: Cart operations
cart.remove_item("P002")  # Remove book
print(f"Items after removal: {cart.get_cart_items()}")

cart.clear_cart()
print(f"Items after clearing: {cart.get_total_items()}")

# Expected outputs should show proper product management, cart operations,
# discount calculations, inventory updates, and business analytics

