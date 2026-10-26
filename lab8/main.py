import os
import json

from product import Product
from inventory import Inventory
from filehandling import FileHandling 

quantity_inp = "0"
product_id = "P001"

filename = 'inventory.txt'
failed_entries = 0
delivery_amount = 0
counter = 0
key = 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "inventory.json")


repository = FileHandling(FILE_PATH)
inventory_entry, load_status = repository.load_inventory()

if load_status == "not_found":
    print("File not found. Starting a fresh inventory.")
elif load_status == "invalid_file":
    print("Saved file could not be read. Starting a fresh inventory.")
else:
    print("Inventory loaded successfully.")


def get_valid_input(inventory_entry, failed_entries: int):
    # 1. FIXED: Access the inventory container from the passed object instance
    next_num = len(inventory_entry.inventory) + 1
    product_id = "P" + str(next_num).zfill(3)

    while True:
        # 2. Validate Product Name
        name = input("Enter Product Name: ").strip()
        if not name:
            print("Error! Product name cannot be blank.\n")
            failed_entries += 1
            continue

        # 3. Validate Price
        price_input = input("Enter Price: ").strip()
        try:
            price = float(price_input)
        except ValueError:
            print("Invalid input. Please enter a valid price.")
            failed_entries += 1
            continue
        if price < 0:
            print("Invalid input. Price cannot be negative.")
            failed_entries += 1
            continue

        # 4. Validate Quantity
        quantity_input = input("Enter Stock Quantity: ").strip()
        if not quantity_input.isdigit() or not (0 <= int(quantity_input) <= 500):
            print("Invalid input. Please enter a number between 0 and 500.")
            failed_entries += 1
            continue
        stock = int(quantity_input)

        # 5. Return the clean, validated variables back to the main loop
        return product_id, name, price, stock, failed_entries






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
            if not inventory_entry.inventory:
                print("Inventory is empty.")
            else:
                print("Current Inventory:")
                print("-" * 60)
                
                # Loop through all Product object instances stored in the dictionary
                inventory_entry.display_all()
                    
                print("-" * 60)
        case 2:
            print("Adding new product...")
            product_id, name, price, stock, failed_entries = get_valid_input(inventory_entry, failed_entries)
            new_product = Product(product_id, name, price, stock)
            delivery_amount, product_id = inventory_entry.add_product(new_product, delivery_amount)
        case 3:
            print("Update Stock")
            # 1. Ask the user for the ID and query our inventory search method
            product_id = input("Enter Product ID to update: ").strip().upper()
            product = inventory_entry.search_product(product_id)
            
            if product is None:
                print("Product not found.")
                failed_entries += 1
            else:
                # 2. If the product object exists, run our updated stock modifier
                # Python automatically maps inventory_entry to 'self' behind the scenes
                delivery_amount, failed_entries = Product.update_stock(
                    inventory_entry, product.product_id, delivery_amount, failed_entries
                )

        case 4:
            print("Searching Product")
            # Call the method on the object instance. 
            # Python automatically passes the instance as 'self' behind the scenes!
            product_id = input("Enter Product ID: ").strip()
            product = inventory_entry.search_product(product_id)

            if product is None:
                print("Product not found")
                failed_entries = inventory_entry.failed_entries
            else:
                print("Product Found")
                print("-" * 60)
                product.display_information()
                print("-" * 60)
                        

        case 5:
            print("Saving inventory...")
            FileHandling.save_inventory(inventory_entry, delivery_amount, FILE_PATH)

        case 6:
            print("Saving inventory before exit.")
            FileHandling.save_inventory(inventory_entry, delivery_amount, FILE_PATH)
            Product.goodbye_message()
            break

        case _:
            print("Invalid option. Please try again.")