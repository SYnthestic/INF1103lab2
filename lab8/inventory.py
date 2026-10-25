import os, json
from product import Product

class Inventory(Product):
    def __init__(self):
        # Initializes an empty list to store the product objects
        self.products = []


    def get_valid_input(failed_entries):
        while True:

            name = input("Enter Product Name: ").strip()
            if not name:
                print("Error! Product name cannot be blank.\n")
                failed_entries += 1
                continue

            price = input("Enter Price: ").strip()
            try:
                price = float(price)
            except ValueError:
                print("Invalid input. Please enter a valid price.")
                failed_entries += 1
                continue
            if price < 0:
                print("Invalid input. Price cannot be negative.")
                failed_entries += 1
                continue

            quantity = input("Enter Quantity: ").strip()
            if not quantity.isdigit() or int(quantity) > 500:
                print("Invalid input. Please enter a number between 0 and 500.")
                failed_entries += 1
                continue

            return product_id, name, price, int(quantity), failed_entries

    def add_product(self, product: Product, delivery_amount: float = 0):
        # 1. Process delivery using the Product class's static method
        # Pass the quantity and delivery amount straight from the object
        processed_delivery = Product.process_delivery(delivery_amount, product.quantity)
        
        # 2. Store the actual Product object directly using its ID as the key
        self.inventory[product.product_id] = product
        
        print(f"Product '{product.name}' added successfully!")
        
        # 3. Calculate what the NEXT product ID should be automatically
        current_numeric_id = int(product.product_id[1:])  # e.g., "P001" -> 1
        next_numeric_id = current_numeric_id + 1          # 1 -> 2
        next_product_id = "P" + str(next_numeric_id).zfill(3)  # 2 -> "P002"
        
        # Return the processed delivery fee and the next suggested ID
        return processed_delivery, next_product_id

    def search_product(self, failed_entries):
            product_id = input("Enter Product ID: ").strip().upper()

            if product_id not in self.inventory:
                print("Product not found")
                return None, failed_entries + 1

            d = self.inventory[product_id]
            print("Product Found")
            print("-" * 60)
            print(f"ID: {product_id}\nName: {d['name']}\nPrice: ${d['price']:.2f}\nStock: {d['quantity']}")
            print("-" * 60)
            return product_id, failed_entries