import os
import json

quantity_inp = "0"
orderid = 1001
inventory_entry = []
filename = 'inventory.txt'
failed_entries = 0
delivery_amount = 0
counter = 0
key = 0








def load_inventory(filename):
    if not os.path.isfile(filename):
        print("File not found. Starting a fresh inventory.")
        return [], 1001

    try:
        print("inventory.txt found")
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

        print(f"Inventory loaded successfully")

        return inventory_entry, next_order_id

    except Exception as e:
        print(f"Error loading inventory: {e}")
        print("Starting a fresh inventory.")
        return [], 1001
        

def display_all(inventory_entry):
    if not inventory_entry:
        print("Inventory is empty.")
        return
    print("Current Inventory:")
    print("-"*60)
    for orderid, product, quantity in inventory_entry:
        print(f"{orderid}, {product}, {quantity}")
    print("-"*60)


def get_valid_input(failed_entries):
    while True:
        product = input("Enter Product Name: ").strip()
        if not product:
            print("Error! Product name cannot be blank.\n")
            failed_entries += 1
            continue

        quantity = input("Enter Quantity: ").strip()
        if not quantity.isdigit():
            print("Invalid input. Please enter a non-negative number.")
            failed_entries += 1
            continue

        quantity = int(quantity)
        if quantity > 500:
            print("Invalid input. Please enter a number between 0 and 500.")
            failed_entries += 1
            continue

        return product, quantity, failed_entries

def add_product(inventory_entry, product, quantity, orderid, delivery_amount):
    if product in [item[1] for item in inventory_entry]:
        print(f"{product} already exists. Use update_stock instead.")
        return orderid, delivery_amount

    inventory_entry.append((orderid, product, quantity))
    delivery_amount = process_delivery(delivery_amount, quantity)

    print("New order added to inventory")
    print(f"{orderid}, {product}, {quantity}")
    return orderid + 1, delivery_amount


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
while key != 6:
    keyverify = False
    while keyverify == False:
        print('''
            ----------- MENU ----------- 
            1. Display All Products 
            2. Add Product 
            3. Update Stock 
            4. Search Product 
            5. Save Inventory 
            6. Exit 
            ----------------------------''')
        key = input("Enter option: ")
        if len(key) == 0:
            print("Empty Response!")
        elif key.isnumeric() == False:
            print("Error! Letters detected!!")
        elif key.isspace():
            print("Error! Space only answer not allowed")
        else:
            keyverify = True
            key = int(key)

    match key:
        case 1:
            display_all(inventory_entry)
        case 2:
            print("Adding new product...")
            product, quantity, failed_entries = get_valid_input(failed_entries)
            orderid, delivery_amount = add_product(
                inventory_entry, product, quantity, orderid, delivery_amount
            )
        case 3:
            print("Updating stock...")
            # update_stock(inventory_entry)
        case 4:
            print("Searching product...")
            # search_product(inventory_entry)
        case 5:
            print("Saving inventory...")
            save_inventory(inventory_entry, delivery_amount)
        case 6:
            print("Exiting the program...")
            generate_report(
                failed_entries,
                inventory_entry,
                delivery_amount
            )
            calculate_tax(delivery_amount)
            save_inventory(inventory_entry, delivery_amount)

            break

        case _:
            print("Invalid option. Please try again.")