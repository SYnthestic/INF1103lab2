from canbeshipped import CanBeShipped
from product import Product


class Inventory:
    """Holds products. It does not extend Product, because it HAS products."""
    def __init__(self):
        self.inventory: list[Product] = []
        self.failed_entries = 0

    def add_product(self, product: Product):
        for existing in self.inventory:
            if existing.product_id == product.product_id:
                raise ValueError(f"Product ID {product.product_id} already exists.")

        self.inventory.append(product)

        delivery_amount = self.process_delivery()
        next_num = len(self.inventory) + 1
        next_id = "P" + str(next_num).zfill(3)
        return delivery_amount, next_id

    def search_product(self, product_id: str) -> Product | None:
        for product in self.inventory:
            if product.product_id == product_id:
                return product
        self.failed_entries += 1
        return None

    #Remove product
    def remove_product(self, product_id: str):
        product = self.search_product(product_id)
        if product is None:
            return None
        self.inventory.remove(product)
        return product

    def display_all(self) -> None:
        for product in self.inventory:
            product.display_information()

    def update_stock(self, product_id: str) -> bool:
        product = self.search_product(product_id)
        if product is None:
            print("Product not found.")
            return False

        qty_input = input("Enter new stock quantity: ").strip()
        if not qty_input.isdigit() or not (0 <= int(qty_input) <= 500):
            print("Invalid stock quantity.")
            return False

        product.stock = int(qty_input)
        print("Stock updated successfully.")
        return True

    def total_shipping_fees(self) -> float:
        total = 0.0
        for product in self.inventory:
            if isinstance(product, CanBeShipped):
                total += product.calculate_shipping_cost()
        return total

    def process_delivery(self) -> int:
        # Replace with your existing delivery calculation logic
        return sum(1 for product in self.inventory if product.stock < 10)
