from canbeshipped import CanBeShipped
from product import Product


class Inventory:
    """Holds products. It does not extend Product, because it HAS products."""
    def __init__(self):
        self.inventory: list[Product] = []
        self.failed_entries = 0

    def add_product(self, product: Product) -> tuple[int, str]:
        """Ensures no duplicate IDs are added, appends the product,

        and returns the next delivery amount along with the lowest unused product ID.
        """
    # 1. Enforce unique ID constraint (prevents index corruption)
        for existing in self.inventory:
            if existing.product_id == product.product_id:
                raise ValueError(f"Product ID {product.product_id} already exists.")

        # 2. Append to our core polymorphic storage list
        self.inventory.append(product)

        # 3. Recalculate operational delivery metrics
        delivery_amount = self.process_delivery()

        # 4. Extract all active ID integers currently in use into a set
        # Example: If inventory has ['P001', 'P003'], used_ids becomes {1, 3}
        used_ids = {int(p.product_id[1:]) for p in self.inventory if p.product_id[1:].isdigit()}

        # 5. Search incrementally starting at 1 to find the absolute lowest gap
        next_num = 1
        while next_num in used_ids:
            next_num += 1

        # 6. Format back to standard zero-padded identifier (e.g., 2 -> 'P002')
        next_id = "P" + str(next_num).zfill(3)

        return delivery_amount, next_id


    def find_product(self, product_id: str) -> Product | None:
        for product in self.inventory:
            if product.product_id == product_id:
                print(product.get_fulfilment_info())
                return product
        self.failed_entries += 1
        return None


    #Remove product
    def remove_product(self, product_id: str):
        product = self.find_product(product_id)
        if product is None:
            return None
        self.inventory.remove(product)
        return product

    def display_all_products(self) -> None:
        for product in self.inventory:
            product.display_information()
            print(product.get_fulfilment_info())

    def update_stock(self, product_id: str) -> bool:
        product = self.find_product(product_id)
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
