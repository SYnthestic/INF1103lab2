import os
import json

quantity_inp = "0"
orderid = 1001
inventory_entry = []
filename = 'inventory.txt'
failed_entries = 0
delivery_amount = 0
counter = 0


import os
import json


def load_inventory(filename):
    if not os.path.isfile(filename):
        print("File not found. Starting a fresh inventory.")
        return [], 1001

    try:
        inventory_entry = []

        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                orderid, product, quantity = line.split(",")

                inventory_entry.append({
                    "orderid": int(orderid.strip().strip("()")),
                    "product": product.strip(),
                    "quantity": int(quantity.strip().strip("()"))
                })

        # Find next order ID
        if inventory_entry:
            existing_ids = [
                item["orderid"]
                for item in inventory_entry
            ]

            next_order_id = max(existing_ids) + 1
        else:
            next_order_id = 1001

        print(f"Inventory loaded successfully. Next Order ID: {next_order_id}")

        return inventory_entry, next_order_id

    except Exception as e:
        print(f"Error loading inventory: {e}")
        print("Starting a fresh inventory.")
        return [], 1001





def get_valid_input(
    failed_entries,
    delivery_amount,
    inventory_entry,
    product_inp,
    orderid
):
    # Keep asking until a valid quantity is entered
    while True:
        quantity_inp = input("Enter Quantity: ").strip()

        if quantity_inp.lower() == "exit":
            print("Please enter a quantity, not 'exit'.")
            continue

        if not quantity_inp.isdigit():
            print(
                "Invalid input. "
                "Please enter a non-negative number."
            )
            failed_entries += 1
            continue

        quantity_inp = int(quantity_inp)

        if quantity_inp > 500:
            print(
                "Invalid input. "
                "Please enter a number between 0 and 500."
            )
            failed_entries += 1
            continue

        # Quantity is valid
        inventory_entry.append((orderid, product_inp, quantity_inp))
        

        delivery_amount = process_delivery(
            delivery_amount,
            quantity_inp
        )

        print(f"New order added to inventory")
        print(f"{orderid}, {product_inp}, {quantity_inp}")
        orderid += 1

        break

    return failed_entries, delivery_amount, orderid


def process_delivery(delivery_amount, entry_inp):
    if entry_inp > 0:
        delivery_amount += entry_inp
        print(f"Delivery amount updated to: {delivery_amount}")
        return delivery_amount

    else:
        print("No delivery amount added for zero or negative entries.")
        return delivery_amount


def calculate_tax(delivery_amount):
    tax_rate = 0.1  # 10% tax rate
    tax_amount = delivery_amount * tax_rate
    return tax_amount


def generate_report(failed_entries, inventory_entry):
    print("\nExiting the program.")
    print(f"Total Units Processed: {len(inventory_entry)}")
    print(f"Transaction History: {inventory_entry}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")

def save_inventory(inventory_list):
    file_name = "inventory.txt"
    
    # Join the list items with a newline character
    # and convert items to strings just in case they are numbers
    content = "\n".join(str(item) for item in inventory_list)
    
    with open(file_name, "w") as file:
        file.write(content)

    print(f"File saved successfully to {file_name}")



while True:

    # Validate menu choice
    while True:
        inventory_entry = load_inventory(filename)
        user_choice = input(
            "Do you want to continue, or do you want to quit "
            "(continue | quit):\n"
        ).strip().lower()

        if user_choice in ("continue", "c", "quit", "exit", "e"):
            break

        print("Error! Please enter 'continue' or 'quit'.\n")

    match user_choice:

        case "continue" | "c":

            # Validate product name
            while True:
                product_inp = input("Enter Product Name: ").strip()

                if product_inp:
                    break

                print("Error! Product name cannot be blank.\n")

            # Use the function to validate quantity
            failed_entries, delivery_amount, orderid = get_valid_input(
                failed_entries,
                delivery_amount,
                inventory_entry,
                product_inp,
                orderid
            )

        case "quit" | "exit" | "e":

            generate_report(
                failed_entries,
                inventory_entry
            )

            save_inventory(inventory_entry)

            break