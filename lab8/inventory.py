import os, json
from product import Product

class Inventory(Product):
    def __init__(self):
        self.inventory = {}


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

    def add_product(inventory, product_id, name, price, quantity, delivery_amount):

            inventory[product_id] = {"name": name, "price": price, "quantity": quantity}
            delivery_amount = Product.process_delivery(delivery_amount, quantity)

            print("Product added successfully!")
            product_id = int(product_id[1:])  # Convert product ID to integer for display]
            product_id += 1  # Increment product ID for the next product
            product_id = "P" + str(product_id).zfill(3)  # Format product ID back to PXXX format
            return delivery_amount, product_id

    def search_product(inventory, failed_entries):
            product_id = input("Enter Product ID: ").strip().upper()

            if product_id not in inventory:
                print("Product not found")
                return None, failed_entries + 1

            d = inventory[product_id]
            print("Product Found")
            print("-" * 60)
            print(f"ID: {product_id}\nName: {d['name']}\nPrice: ${d['price']:.2f}\nStock: {d['quantity']}")
            print("-" * 60)
            return product_id, failed_entries