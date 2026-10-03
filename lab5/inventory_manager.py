import os
import json

quantity_inp = "0"
product_id = "P001"
inventory_entry = {}
filename = 'inventory.txt'
failed_entries = 0
delivery_amount = 0
counter = 0
key = 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "inventory.json")








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
        

def display_all(inventory):
    if not inventory:
        print("Inventory is empty.")
        return
    print("Current Inventory:")
    print("-" * 60)
    for product_id, d in inventory.items():
        print(f"ID: {product_id} | Name: {d['name']} | Price: ${d['price']:.2f} | Stock: {d['quantity']}")
    print("-" * 60)


def get_valid_input(failed_entries):
    while True:

        name = input("Enter Product Name: ").strip()
        if not name:
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
        if not quantity.isdigit() or int(quantity) > 500:
            print("Invalid input. Please enter a number between 0 and 500.")
            failed_entries += 1
            continue

        return product_id, name, price, int(quantity), failed_entries

def add_product(inventory, product_id, name, price, quantity, delivery_amount):

    inventory[product_id] = {"name": name, "price": price, "quantity": quantity}
    delivery_amount = process_delivery(delivery_amount, quantity)

    print("Product added successfully!")
    product_id = int(product_id[1:])  # Convert product ID to integer for display]
    product_id += 1  # Increment product ID for the next product
    product_id = "P" + str(product_id).zfill(3)  # Format product ID back to PXXX format
    return delivery_amount, product_id


def process_delivery(delivery_amount, quantity_inp):
    if int(quantity_inp) > 0:
        delivery_amount += int(quantity_inp)
        print(f"Delivery amount updated to: {delivery_amount}")
        return delivery_amount

    else:
        print("No delivery amount added for zero or negative entries.")
        return delivery_amount

def update_stock(inventory, product_id, delivery_amount, failed_entries):
    if product_id is None:
        return delivery_amount, failed_entries

    name = inventory[product_id]["name"]
    new_quantity = input(f"New Stock Quantity: ").strip()

    if not new_quantity.isdigit() or int(new_quantity) > 500:
        print("Invalid input. Please enter a number between 0 and 500.")
        return delivery_amount, failed_entries + 1

    new_quantity = int(new_quantity)
    old_quantity = inventory[product_id]["quantity"]
    inventory[product_id]["quantity"] = new_quantity
    delivery_amount += new_quantity - old_quantity

    print(f"Stock updated successfully!")
    return delivery_amount, failed_entries


def calculate_tax(delivery_amount):
    tax_rate = 0.1  # 10% tax rate
    tax_amount = delivery_amount * tax_rate
    print("Tax Amount is: ${}".format(tax_amount))
    return tax_amount


def save_inventory(inventory, delivery_amount, file_name):
    data = {
        "delivery_amount": delivery_amount,
        "inventory": inventory,
    }

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Inventory saved successfully to inventory.json")


def search_product(inventory, failed_entries):
    product_id = input("Enter Product ID: ").strip().upper()

    if product_id not in inventory:
        print("Product not found")
        return None, failed_entries + 1

    d = inventory[product_id]
    print("Product Found")
    print("-" * 60)
    print(f"ID: {product_id}\nName: {d['name']}\nPrice: ${d['price']:.2f}\nStock: {d['quantity']}")
    print("-" * 60)
    return product_id, failed_entries

def goodbye_message():
        print('''
Thank you for using Inventory Management System.
Program terminated.''')





product_id, inventory_entry, delivery_amount = load_inventory(FILE_PATH)
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
            product_id, name, price, quantity, failed_entries = get_valid_input(failed_entries)
            delivery_amount, product_id = add_product(
                inventory_entry, product_id, name, price, quantity, delivery_amount
            )
        case 3:
            print("Update Stock")
            product_id, failed_entries = search_product(inventory_entry, failed_entries)
            delivery_amount, failed_entries = update_stock(
                inventory_entry, product_id, delivery_amount, failed_entries
            )
        case 4:
            print("Searching Product")
            _, failed_entries = search_product(inventory_entry, failed_entries)
        case 5:
            print("Saving inventory...")
            save_inventory(inventory_entry, delivery_amount, FILE_PATH)
        case 6:
            print("Saving inventory before exit.")
            save_inventory(inventory_entry, delivery_amount, FILE_PATH)
            goodbye_message()

            break

        case _:
            print("Invalid option. Please try again.")