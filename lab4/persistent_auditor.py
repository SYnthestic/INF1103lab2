import os
import json

quantity_inp = "0"
orderid = 1001
inventory_entry = []
filename = 'inventory.txt'
failed_entries = 0
delivery_amount = 0
counter = 0


def load_inventory(filename):
    # 3. CRITICAL CHANGE: If file DOES NOT exist, start fresh with orderid 1001
    if not os.path.isfile(filename):
        print(f"File not found. Starting a fresh inventory with Order ID: 1001")
        return [], 1001, filename

    # 4. If file EXISTS, try to read it
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        # 5. Find the next order_id based on existing data
        if data and isinstance(data, list):
            # Extract all order_id values from the list of dictionaries
            # Defaults to 1000 if "order_id" keys are somehow missing
            existing_ids = [item.get("order_id", 1001) for item in data]
            next_order_id = max(existing_ids) + 1
        else:
            # File exists but is empty array []
            next_order_id = 1001

        print(
            f"Data successfully loaded. Resuming from Order ID: {next_order_id}."
        )
        return data, next_order_id, filename

    except Exception as e:
        print(f"An error occurred: {e}. Starting fresh.")
        return [], 1001, filename


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