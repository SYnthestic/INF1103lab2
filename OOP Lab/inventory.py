import os, json
from product import Product
from canbeshipped import CanBeShipped

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
            product.display_information()
            
        print("-" * 60)



    def add_product(self, product: Product):
        self.validate_stock(product, product.stock)

        self.inventory[product.product_id] = product
        print(f"Product '{product.name}' added successfully!")

        processed_delivery = Product.process_delivery(self)

        current_numeric_id = int(product.product_id[1:])      # "P001" -> 1
        next_product_id = "P" + str(current_numeric_id + 1).zfill(3)

        return processed_delivery, next_product_id

    def validate_stock(self, product, quantity: int) -> None:
        """Validated setter. Raises TypeError / ValueError on bad input."""
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("Quantity must be a whole number.")
        if not 0 <= quantity <= 500:
            raise ValueError("Quantity must be between 0 and 500.")
        
        product.stock = quantity 

    def update_stock(self, product_id: str) -> bool:
        """Finds product by ID, gathers user input, and validates update."""
        product = self.inventory.get(product_id)
        
        if not product:
            print(f"Error: Product {product_id} not found.")
            return False

        try:
            new_qty = int(input("Enter new stock quantity: ").strip())
            # Forward the product instance over to your moved validation method
            self.validate_stock(product, new_qty)
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
            return False

        print(f"Stock updated. New stock: {product.stock}")
        return True


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

    def total_shipping_fees(self) -> float:
        """Calculates the total monetary shipping fees for all shippable items."""
        total_fee = 0.0
        for product in self.inventory.values():
            # Safeguard: only trigger calculation for shippable items
            if isinstance(product, CanBeShipped):
                total_fee += product.calculate_shipping_cost() * product.stock
        return total_fee

    