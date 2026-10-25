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
            Product.display_information(inventory_entry)
        case 2:
            print("Adding new product...")
            product_id, name, price, quantity, failed_entries = Inventory.get_valid_input(failed_entries)
            delivery_amount, product_id = Inventory.add_product(
                inventory_entry, product_id, name, price, quantity, delivery_amount
            )
        case 3:
            print("Update Stock")
            product = inventory_entry.search_product(input("Enter Product ID: "))
            
            if product is not None:
                inventory_entry.update_stock(product, new_quantity)
        case 4:
            print("Searching Product")
            # Call the method on the object instance. 
            # Python automatically passes the instance as 'self' behind the scenes!
            product_id = input("Enter Product ID: ")
            product = inventory_entry.search_product(product_id)

            if product is None:
                print("Product not found")
            else:
                print("Product Found")
                print("-" * 60)
                print(product.details())
                print("-" * 60)
                        

        case 5:
            print("Saving inventory...")
            repository.save_inventory(inventory_entry)

        case 6:
            print("Saving inventory before exit.")
            if repository.save_inventory(inventory_entry):
                print("Inventory saved successfully.")
            else:
                print("Could not save the inventory.")
            Product.goodbye_message()
            break

        case _:
            print("Invalid option. Please try again.")