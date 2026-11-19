import json
import os
import csv

import products  # noqa: F401  (auto-imports every module in products/ so they register)
from productfactory import ProductFactory
from inventory import Inventory
from order import Order
from product_registry import get_product_types
from supplier import Supplier


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

## Load .json
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

            raw_inventory = data.get("inventory", [])

            # Support both dict format {product_id: details} and list format [details, ...]
            if isinstance(raw_inventory, dict):
                entries = raw_inventory.items()
            elif isinstance(raw_inventory, list):
                entries = [(item.get("product_id", ""), item) for item in raw_inventory]
            else:
                return Inventory(), "invalid_file"

            for product_id, details in entries:
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

## SAve .json
    @staticmethod
    def save_inventory(inventory: Inventory, delivery_amount, file_name: str) -> None:
        product_list = inventory.inventory if hasattr(inventory, "inventory") else inventory

        serialized_inventory = {
            product.product_id: product.to_dict() for product in product_list
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

    # Load .csv
    def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None: 
        try: 
            file = open(path, newline="") 
        except FileNotFoundError: 
            print(f"Products file not found: {path}") 
        else:  #This activates only if the file is proven to exist. Obviously first run the file won't exist, so we need to save it as products.csv
            loaded = 0
            with file: 
            # read rows with csv.reader and skip the header row 
                reader = csv.reader(file)
                next(reader, None)
            # for each row: try to create and add the product, 
                for row in reader:
                    try: 
                        product_type, product_id, name, price, stock_quantity = row
                        product = ProductFactory.create(
                            product_type.strip().lower(),
                            product_id.strip(),
                            name.strip(),
                            float(price),
                            int(stock_quantity),
                            supplier
                        )
                        inventory.add_product(product)
                        loaded += 1
            # except ValueError: report the row and continue 
                    except ValueError as e:
                        print(f"Unable to add row {row}: {e}")
            print(f"{loaded} products loaded.") 
        finally: 
            print("Load attempt finished.")

    # Save .csv
    @staticmethod
    def save_products(path: str, inventory: Inventory) -> None:
        try:
            file = open(path, mode="w", newline="", encoding="utf-8")
        except OSError as e:
            print(f"Error opening products file for saving ({path}): {e}")
        else:
            saved = 0
            # Build reverse lookup: {PhysicalProduct: "physical", SubscriptionProduct: "subscription", ...}
            type_lookup = {cls: label.lower() for label, cls in get_product_types().items()}

            with file:
                writer = csv.writer(file)
                # 1. Write the header row (matching load_products column order)
                writer.writerow(["product_type", "product_id", "name", "price", "stock_quantity"])

                # 2. Loop through products in inventory and write each row
                for product in inventory.inventory:
                    product_type = type_lookup.get(
                        type(product),
                        type(product).__name__.replace("Product", "").lower()
                    )

                    writer.writerow([
                        product_type,
                        product.product_id,
                        product.name,
                        product.price,
                        product.stock
                    ])
                    saved += 1

            print(f"{saved} products saved.")
        finally:
            print("Save attempt finished.")

## Orders
    @staticmethod
    def save_orders(orders: list[Order], file_name: str) -> None:
        serialized_orders = [order.to_dict() for order in orders]

        if os.path.dirname(file_name):
            os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, "w", encoding="utf-8") as file:
            json.dump({"orders": serialized_orders}, file, indent=4)

        print("Orders saved successfully.")

    @staticmethod
    def load_orders(file_name: str, inventory: Inventory) -> list[Order]:
        if not os.path.isfile(file_name):
            return []

        try:
            with open(file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
            return [Order.from_dict(item, inventory) for item in data.get("orders", [])]
        except (OSError, ValueError, KeyError, TypeError) as error:
            print(f"DEBUG order load error: {type(error).__name__}: {error}")
            return []

