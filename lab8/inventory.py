import os, json
from product import Product

class Inventory:
    """Holds products. It does not extend Product, because it HAS products."""

    def __init__(self):
        self.inventory = {}         
        self.failed_entries = 0

    def display_all(self) -> None:
        """Loops through the collection and delegates printing to each Product object."""
        if not self.inventory:
            print("Inventory is empty.")
            return

        print("Current Inventory:")
        print("-" * 60)
        
        for product in self.inventory.values():
            # 🟢 OOP Delegation: Tell the product instance to print itself!
            product.display_information()
            
        print("-" * 60)



    def add_product(self, product: Product):
        # 1. Store the product first so it's included in the total
        self.inventory[product.product_id] = product
        print(f"Product '{product.name}' added successfully!")

        # 2. Recalculate delivery from EVERYTHING in the dictionary
        processed_delivery = Product.process_delivery(self)

        # 3. Calculate the next product ID
        current_numeric_id = int(product.product_id[1:])      # "P001" -> 1
        next_product_id = "P" + str(current_numeric_id + 1).zfill(3)

        return processed_delivery, next_product_id

    def next_product_id(self) -> str:
        numbers = [int(pid[1:]) for pid in self.__products if pid[1:].isdigit()]
        return f"P{(max(numbers) + 1 if numbers else 1):03d}"

    def search_product(self, product_id: str):
        """Returns the Product, or None. Counts a failed search itself."""
        product = self.inventory.get(product_id.strip().upper())
        if product is None:
            self.failed_entries += 1
        return product

    def total_delivery(self) -> int:
        return sum(product.stock for product in self.inventory.values())