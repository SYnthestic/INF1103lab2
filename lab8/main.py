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
from product import Product
from inventory import Inventory
from filehandling import FileHandling 

product_id, inventory_entry, delivery_amount = FileHandling.load_inventory(FILE_PATH)




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
            product_id, failed_entries = Inventory.search_product(inventory_entry, failed_entries)
            delivery_amount, failed_entries = Product.update_stock(
                inventory_entry, product_id, delivery_amount, failed_entries
            )
        case 4:
            print("Searching Product")
            _, failed_entries = Inventory.search_product(inventory_entry, failed_entries)
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