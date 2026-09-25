
import os
import json

quantity_inp = "0"
orderid = 1001
inventory_entry = []
filename = ''
failed_entries = 0
delivery_amount = 0
counter = 0


def load_previous_data(jsonfile_name):
    # Keep asking until a valid, non-empty filename is provided
    while not jsonfile_name:
        jsonfile_name = input(
            "Please provide a valid JSON file name to load the data from: "
        ).strip()

        if not jsonfile_name:
            print("Filename cannot be blank.")

    # Automatically add .json extension if it is missing
    if not str(jsonfile_name).endswith(".json"):
        jsonfile_name = str(jsonfile_name) + ".json"

    # Check whether the file exists
    if not os.path.isfile(jsonfile_name):
        print("This file does not exist.")
        return [], jsonfile_name

    try:
        with open(jsonfile_name, "r", encoding="utf-8") as file:
            data = json.load(file)

        print(f"Data successfully loaded from {jsonfile_name}.")
        return data, jsonfile_name

    except Exception as e:
        print(
            f"An error occurred while loading data from "
            f"{jsonfile_name}: {e}"
        )
        return [], jsonfile_name


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

        quantity = int(quantity_inp)

        if quantity > 500:
            print(
                "Invalid input. "
                "Please enter a number between 0 and 500."
            )
            failed_entries += 1
            continue

        # Quantity is valid
        inventory_entry.append((orderid, product_inp, quantity))
        orderid += 1

        delivery_amount = process_delivery(
            delivery_amount,
            quantity
        )

        print(f"New order added to inventory")
        print(f"{orderid}, {product_inp}, {quantity}")

        break

    return failed_entries, delivery_amount


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


while True:

    # Validate menu choice
    while True:
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
            failed_entries, delivery_amount = get_valid_input(
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

            break


