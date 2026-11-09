import json
import os

import products  # noqa: F401  (auto-imports every module in products/ so they register)
from inventory import Inventory
from product_registry import get_product_types


class FileHandling:
    """Loads and saves an Inventory. It owns the file path and never prints."""

    def __init__(self, path: str):
        self._path = path

    @property
    def path(self) -> str:
        return self._path

    @staticmethod
    def _classes_by_type() -> dict:
        """Maps saved type tags ("digital", "subscription", ...) to product classes."""
        return {cls.type_name: cls for cls in get_product_types().values()}

    def load_inventory(self) -> tuple[Inventory, str]:
        """Returns (inventory, status): "loaded", "not_found" or "invalid_file".
        The inventory is always a valid Inventory, empty if loading failed."""
        inventory = Inventory()
        if not os.path.isfile(self._path):
            return inventory, "not_found"

        classes = self._classes_by_type()

        try:
            with open(self._path, "r", encoding="utf-8") as file:
                data = json.load(file)

            for product_id, details in data["inventory"].items():
                # 1. Deduce the product type from modern tag or legacy keys
                product_type = details.get("type")
                if not product_type:
                    if "download_size" in details:
                        product_type = "digital"
                    else:
                        product_type = "physical"

                # 2. Let the matching class build itself (no if/elif chain)
                product_class = classes.get(product_type)
                if product_class is None:
                    continue  # Skip unknown custom formats entirely

                product = product_class.from_dict(product_id, details)

                # 3. Safe integration check: Do not let a single legacy product's bad
                # stock crash the entire file import sequence.
                try:
                    _processed_delivery, _next_id = inventory.add_product(product)
                except (ValueError, TypeError) as val_error:
                    print(f"DEBUG skip product {product_id}: {val_error}")
                    continue

        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            print(f"DEBUG load error: {type(error).__name__}: {error}")
            return Inventory(), "invalid_file"

        return inventory, "loaded"

    @staticmethod
    def save_inventory(inventory, delivery_amount, file_name):
        # 1. Safely extract the inner products dictionary from the Inventory instance
        if hasattr(inventory, '_products'):
            inv_dict = inventory._products
        elif hasattr(inventory, 'products'):
            inv_dict = inventory.products
        elif hasattr(inventory, 'inventory'):
            inv_dict = inventory.inventory
        else:
            inv_dict = inventory

        # 2. Each product describes its own saved form
        serialized_inventory = {
            p_id: product.to_dict() for p_id, product in inv_dict.items()
        }

        data = {
            "delivery_amount": delivery_amount,
            "inventory": serialized_inventory,
        }

        if os.path.dirname(file_name):
            os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Inventory saved successfully.")