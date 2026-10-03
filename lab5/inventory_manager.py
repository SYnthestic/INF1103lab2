import os
import json

quantity_inp = "0"
orderid = 1001
inventory_entry = {}
filename = 'inventory.txt'
failed_entries = 0
delivery_amount = 0
counter = 0
key = 0








def load_inventory(file_name):
    if not os.path.isfile(file_name):
        print("File not found. Starting a fresh inventory.")
        return {}, 1001, 0

    try:
        with open(file_name, "r") as file:
            data = json.load(file)

        inventory = data["inventory"]
        delivery_amount = data["delivery_amount"]

        ids = [d["orderid"] for d in inventory.values()]
        next_order_id = max(ids) + 1 if ids else 1001

        print("Inventory loaded successfully")
        return inventory, next_order_id, delivery_amount

    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading inventory: {e}")
        print("Starting a fresh inventory.")
        return {}, 1001, 0
        

def display_all(inventory_entry):
    if not inventory_entry:
        print("Inventory is empty.")
        return
    print("Current Inventory:")
    print("-"*60)
    for product, details in inventory_entry.items():
        print(f"ID: {details['orderid']} | Name: {product} | Price: ${details['price']:.2f} | Stock: {details['quantity']}")
    print("-"*60)


def get_valid_input(failed_entries):
    while True:
        product = input("Enter Product Name: ").strip()
        if not product:
            print("Error! Product name cannot be blank.\n")
            failed_entries += 1
            continue

        price = input("Enter Price: ").strip()
        try:
            price = float(price)
        except ValueError:
            print("Invalid input. Please enter a valid price.")
            failed_entries += 1
            continue

        if price < 0:
            print("Invalid input. Price cannot be negative.")
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

        return product, price, quantity, failed_entries

def add_product(inventory_entry, product, price, quantity, orderid, delivery_amount):
    if product in inventory_entry:
        print(f"{product} already exists. Use update_stock instead.")
        return orderid, delivery_amount

    inventory_entry[product] = {
        "orderid": orderid,
        "price": price,
        "quantity": quantity
    }
    delivery_amount = process_delivery(delivery_amount, quantity)

    print("Product added successfully!")
    print(f"{orderid}, {product}, ${price:.2f}, {quantity}")
    return orderid + 1, delivery_amount


def process_delivery(delivery_amount, quantity_inp):
    if int(quantity_inp) > 0:
        delivery_amount += int(quantity_inp)
        print(f"Delivery amount updated to: {delivery_amount}")
        return delivery_amount

    else:
        print("No delivery amount added for zero or negative entries.")
        return delivery_amount

def update_stock(inventory, name, delivery_amount, failed_entries):
    if name is None:
        return delivery_amount, failed_entries

    new_quantity = input(f"New stock quantity for {name}: ").strip()

    if not new_quantity.isdigit() or int(new_quantity) > 500:
        print("Invalid input. Please enter a number between 0 and 500.")
        return delivery_amount, failed_entries + 1

    new_quantity = int(new_quantity)
    old_quantity = inventory[name]["quantity"]

    inventory[name]["quantity"] = new_quantity
    delivery_amount += new_quantity - old_quantity

    print(f"Stock updated for {name}. New quantity: {new_quantity}")
    return delivery_amount, failed_entries


def calculate_tax(delivery_amount):
    tax_rate = 0.1  # 10% tax rate
    tax_amount = delivery_amount * tax_rate
    print("Tax Amount is: ${}".format(tax_amount))
    return tax_amount


def save_inventory(inventory, delivery_amount, file_name="inventory.json"):
    data = {
        "delivery_amount": delivery_amount,
        "inventory": inventory,
    }
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Inventory saved successfully to {file_name}")


def search_product(inventory, failed_entries):
    id_text = input("Enter product ID: ").strip()

    if not id_text.isdigit():
        print("Invalid input. Please enter a numeric ID.")
        return None, failed_entries + 1

    order_id = int(id_text)

    for name, details in inventory.items():
        if details["orderid"] == order_id:
            print("Product Found")
            print("-" * 60)
            print(f"ID: {order_id}\nName: {name}\nPrice: ${details['price']:.2f}\nStock: {details['quantity']}")
            print("-" * 60)
            return name, failed_entries

    print("Product not found")
    return None, failed_entries

def goodbye_message():
        print('''
Thank you for using Inventory Management System.
Program terminated.''')





inventory_entry, orderid, delivery_amount = load_inventory(filename)
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
            product, price, quantity, failed_entries = get_valid_input(failed_entries)
            orderid, delivery_amount = add_product(
                inventory_entry, product, price, quantity, orderid, delivery_amount
            )
        case 3:
            print("Update Stock")
            product, failed_entries = search_product(inventory_entry, failed_entries)
            delivery_amount, failed_entries = update_stock(
                inventory_entry, product, delivery_amount, failed_entries
            )
        case 4:
            print("Searching Product")
            search_product(inventory_entry, failed_entries)
        case 5:
            print("Saving inventory...")
            save_inventory(inventory_entry, delivery_amount)
        case 6:
            print("Saving inventory before exit.")
            save_inventory(inventory_entry, delivery_amount)
            goodbye_message()

            break

        case _:
            print("Invalid option. Please try again.")