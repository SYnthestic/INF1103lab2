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
    if not os.path.isfile(filename):
        print("File not found. Starting a fresh inventory.")
        return [], 1001

    try:
        inventory_entry = []

        with open(filename, "r") as file:
            for line in file:
                oline = line.strip()

                if not line:
                    continue

                # Read the saved total
                if oline.startswith("Total quantity:"):
                    delivery_amount = int(
                        oline.split(":")[1].strip()
                    )
                    continue

                orderid, product, quantity = line.split(",")

                inventory_entry.append(( int(orderid.strip()), product.strip(), int(quantity.strip()) ))

        # Find next order ID
        if inventory_entry:
            existing_ids = [
                item[0]
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
    orderid
):
    while True:

        # Display current orders
        print("Current Orders:")

        for stored_orderid, product, order_quantity in inventory_entry:
            print(
                f"{stored_orderid}, "
                f"{product}, "
                f"{order_quantity}"
            )

        print(f"Total quantity: {delivery_amount}")

        # Validate product name
        product_inp = input(
            "Enter Product Name: "
        ).strip()

        if not product_inp:
            print("Error! Product name cannot be blank.\n")
            failed_entries += 1
            continue

        # Validate quantity
        quantity_inp = input(
            "Enter Quantity: "
        ).strip()

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

        # Add complete order
        inventory_entry.append(
            (orderid, product_inp, quantity_inp)
        )

        # Update total quantity
        delivery_amount = process_delivery(
            delivery_amount,
            quantity_inp
        )

        print("New order added to inventory")
        print(
            f"{orderid}, "
            f"{product_inp}, "
            f"{quantity_inp}"
        )

        # Move to next order ID
        orderid += 1

        break

    return failed_entries, delivery_amount, orderid


def process_delivery(delivery_amount, quantity_inp):
    if int(quantity_inp) > 0:
        delivery_amount += int(quantity_inp)
        print(f"Delivery amount updated to: {delivery_amount}")
        return delivery_amount

    else:
        print("No delivery amount added for zero or negative entries.")
        return delivery_amount


def calculate_tax(delivery_amount):
    tax_rate = 0.1  # 10% tax rate
    tax_amount = delivery_amount * tax_rate
    print("Tax Amount is: ${}".format(tax_amount))
    return tax_amount


def generate_report(failed_entries, inventory_entry, delivery_amount):
    print("\nExiting the program.")
    print(f"Total Units Processed: {len(inventory_entry)}")
    print("Transaction History:")
    for stored_orderid, product, quantity in inventory_entry:
        print(f"{stored_orderid}, {product}, {quantity}")
    print("Total Transaction Amount: {}".format(delivery_amount))
    print(f"Number of Failed/Rejected Entries: {failed_entries}")

def save_inventory(inventory_list, delivery_amount):
    file_name = "inventory.txt"

    with open(file_name, "w") as file:
        file.write(f"Total quantity: {delivery_amount}\n")

        for orderid, product, quantity in inventory_list:
            file.write(f"{orderid}, {product}, {quantity}\n")

    print(f"File saved successfully to {file_name}")


inventory_entry, orderid = load_inventory(filename)
for stored_orderid, product, order_quantity in inventory_entry:
    delivery_amount += order_quantity
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

            # Use the function to validate quantity
            failed_entries, delivery_amount, orderid = get_valid_input(
                                failed_entries,
                                delivery_amount,
                                inventory_entry,
                                orderid
                                        )
            # process_delivery(delivery_amount, quantity_inp)

        case "quit" | "exit" | "e":

            generate_report(
                failed_entries,
                inventory_entry,
                delivery_amount
            )
            calculate_tax(delivery_amount)
            save_inventory(inventory_entry, delivery_amount)

            break