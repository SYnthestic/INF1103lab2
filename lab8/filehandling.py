import json
import os

from inventory import Inventory
from product import Product


class FileHandling:
    """Loads and saves an Inventory. It owns the file path and never prints."""

    def __init__(self, path: str):
        self._path = path

    @property
    def path(self) -> str:
        return self._path

    def load_inventory(self) -> tuple[Inventory, str]:
        """Returns (inventory, status): "loaded", "not_found" or "invalid_file".
        The inventory is always a valid Inventory, empty if loading failed."""
        inventory = Inventory()
        if not os.path.isfile(self._path):
            return inventory, "not_found"

        try:
            with open(self._path, "r", encoding="utf-8") as file:
                data = json.load(file)
            for product_id, details in data["inventory"].items():
                inventory.add_product(
                    Product(
                        product_id,
                        details["name"],
                        float(details["price"]),
                        int(details["quantity"]),
                    )
                )
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            print(f"DEBUG load error: {type(error).__name__}: {error}")
            return Inventory(), "invalid_file"
        return inventory, "loaded"

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