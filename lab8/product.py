import os
import json

class Product:
    def __init__(self, product_id: str, name: str, price: float, quantity: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__quantity = quantity

    # Public getters using property decorators
    @property
    def product_id(self): return self.__product_id

    @property
    def name(self): return self.__name

    @property
    def price(self): return self.__price

    # Getter and Setter for quantity so update_stock can modify it
    @property
    def quantity(self): return self.__quantity
    
    @quantity.setter
    def quantity(self, value: int): self.__quantity = value

    # 1. FIXED: Prints this SPECIFIC product instance's details
    def display_information(self) -> None:
        print(
            f"ID: {self.product_id} | "
            f"Name: {self.name} | "
            f"Price: ${self.price:.2f} | "
            f"Stock: {self.quantity}"
        )

    # 2. FIXED: Marked as @staticmethod since it acts as a utility calculation
    @staticmethod
    def process_delivery(delivery_amount: float, quantity_inp: int) -> float:
        qty = int(quantity_inp)
        delivery = float(delivery_amount)

        if qty > 0:
            delivery += qty
            print(f"Delivery amount updated to: {delivery}")
            return delivery  
        else:
            print("No delivery amount added for zero or negative entries.")
            return delivery

    # 3. FIXED: Changed dictionary syntax to object attributes and property setters
    @staticmethod
    def update_stock(inventory, product_id, delivery_amount, failed_entries):
        # Handle cases where inventory is an Inventory class instance or raw dictionary
        inv_dict = inventory.inventory if hasattr(inventory, 'inventory') else inventory

        if product_id is None or product_id not in inv_dict:
            return delivery_amount, failed_entries

        product = inv_dict[product_id]
        new_quantity = input("New Stock Quantity: ").strip()

        if not new_quantity.isdigit() or int(new_quantity) > 500:
            print("Invalid input. Please enter a number between 0 and 500.")
            return delivery_amount, failed_entries + 1

        new_quantity = int(new_quantity)
        old_quantity = product.quantity
        
        # Updates the encapsulated quantity variable via the setter property
        product.quantity = new_quantity
        delivery_amount += new_quantity - old_quantity

        print("Stock updated successfully!")
        return delivery_amount, failed_entries

    # 4. FIXED: Marked as @staticmethod
    @staticmethod
    def calculate_tax(delivery_amount):
        tax_rate = 0.1  
        tax_amount = delivery_amount * tax_rate
        print(f"Tax Amount is: ${tax_amount:.2f}")
        return tax_amount

    # 5. FIXED: Serializes full Product objects into readable JSON formats
    @staticmethod
    def save_inventory(inventory, delivery_amount, file_name):
        inv_dict = inventory.inventory if hasattr(inventory, 'inventory') else inventory
        
        # Convert Product objects into clear dictionary data format for JSON storage
        serialized_inventory = {}
        for p_id, product in inv_dict.items():
            serialized_inventory[p_id] = {
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity
            }

        data = {
            "delivery_amount": delivery_amount,
            "inventory": serialized_inventory,
        }

        if os.path.dirname(file_name):
            os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

        print("Inventory saved successfully.")

    # 6. FIXED: Marked as @staticmethod
    @staticmethod
    def goodbye_message():
        print('''
    Thank you for using Inventory Management System.
    Program terminated.''')
