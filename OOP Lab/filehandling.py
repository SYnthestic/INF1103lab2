import json
import os

from products.digitalproduct import DigitalProduct
from inventory import Inventory
from products.physicalproduct import PhysicalProduct
from products.subscriptionproduct import SubscriptionProduct


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
                # 1. Deduce the product type from modern tag or legacy keys
                product_type = details.get("type")
                if not product_type:
                    if "download_size" in details:
                        product_type = "digital"
                    else:
                        product_type = "physical"

                # 2. Build the correct modern object structure
                if product_type == "physical":
                    weight = float(details.get("weight", 0.0))
                    product = PhysicalProduct(
                        product_id,
                        details["name"],
                        float(details["price"]),
                        int(details["stock"]),
                        weight
                    )
                elif product_type == "digital":
                    size = float(details.get("download_size", 0.0)) 
                    product = DigitalProduct(
                        product_id,
                        details["name"],
                        float(details["price"]),
                        int(details["stock"]),
                        download_size=size
                    )
                elif product_type == "subscription":
                    product = SubscriptionProduct(
                        product_id,
                        details["name"],
                        float(details["price"]),
                        int(details["stock"]),
                        int(details["duration_months"]),
                    )
                else:
                    continue # Skip unknown custom formats entirely

                # 3. Safe integration check: Do not let a single legacy product's bad 
                # stock crash the entire file import sequence.
                try:
                    # Capturing the returned tuple unpack so Python doesn't throw a ValueError
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
        
        serialized_inventory = {}
        for p_id, product in inv_dict.items():
            product_data = {
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            }

            # 2. Inject subclass parameters
            if isinstance(product, DigitalProduct):
                product_data["type"] = "digital"
                product_data["download_size"] = product.download_size
            elif isinstance(product, PhysicalProduct):
                product_data["type"] = "physical"
                product_data["weight"] = product.weight
            elif isinstance(product, SubscriptionProduct):
                product_data["type"] = "subscription"
                product_data["duration_months"] = product.duration_months
            else:
                pass  # Leaves out 'type' for legacy generic objects

            serialized_inventory[p_id] = product_data

        data = {
            "delivery_amount": delivery_amount,
            "inventory": serialized_inventory,
        }

        if os.path.dirname(file_name):
            os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Inventory saved successfully.")
