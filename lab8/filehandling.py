import json
import os


class FileHandling:
    
    def __init__(self, filename):
        self.filename = filename

    def save_inventory(inventory, delivery_amount, file_name):
        data = {
            "delivery_amount": delivery_amount,
            "inventory": inventory,
        }

        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

    print(f"Inventory saved successfully to inventory.json")

    def load_inventory(file_name):
            if not os.path.isfile(file_name):
                print("File not found. Starting a fresh inventory.")
                return "P001", {}, 0
    
            try:
                print("inventory.json found.")
                with open(file_name, "r") as file:
                    data = json.load(file)
                print("Inventory loaded successfully")
                most_recent_id = max(int(pid[1:]) for pid in data["inventory"]) + 1
                product_id = f"P{most_recent_id:03d}"
                return product_id, data["inventory"], data["delivery_amount"]
    
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading inventory: {e}")
                print("Starting a fresh inventory.")
                return "P001", {}, 0