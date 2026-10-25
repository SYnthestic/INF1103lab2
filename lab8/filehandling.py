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

    def save_inventory(self, inventory: Inventory) -> bool:
        data = {
            "delivery_amount": inventory.delivery_amount,
            "inventory": {
                p.product_id: {"name": p.name, "price": p.price, "quantity": p.quantity}
                for p in inventory
            },
        }
        tmp_path = self._path + ".tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            os.replace(tmp_path, self._path)
            return True
        except OSError:
            return False