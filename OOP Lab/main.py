import os

from digitalproduct import DigitalProduct
from filehandling import FileHandling
from physicalproduct import PhysicalProduct
from product import Product

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

def display_goodbye_message():
    print('''
    Thank you for using Inventory Management System.
    Program terminated.''')






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
                # Loop through all Product object instances stored in the dictionary
                inventory_entry.display_all()
                    
                print("-" * 60)
        case 2:
            print("Adding new product...")
            product_id, name, price, stock, failed_entries = get_valid_input(inventory_entry, failed_entries)
            
            print("Select Product Type:")
            print("1. Physical Product")
            print("2. Digital Product")
            user_choice = input("Enter choice (1-2): ").strip()
            
            is_digital = (user_choice == "2") 
            is_physical = (user_choice == "1")
            product_class = DigitalProduct if is_digital else PhysicalProduct
            
            try:
                new_product = product_class.from_ui(product_id, name, price, stock)

                if is_physical:
                    # Triggers your custom weight calculation formulas
                    product_fee = new_product.calculate_shipping_cost()
                    print(f"This item's shipping cost: ${product_fee:.2f}")

                # Your original stock-based delivery logic remains completely untouched here
                delivery_amount, next_id = inventory_entry.add_product(new_product)
                print(new_product.get_fulfilment_info()) 

                # If you need to print the combined shipping costs for the whole inventory:
                print(f"Total Inventory Shipping Fees: ${inventory_entry.total_shipping_fees():.2f}")

                
            except (ValueError, TypeError) as validation_err:
                print(f"Insertion Error: {validation_err}")
                # Keep track of bad operational steps if your lab tracks them
                failed_entries += 1 


        case 3:
            print("Update Stock")
            target_id = input("Enter Product ID to update stock: ").strip()

            # 1. Check if the ID is empty before doing anything else
            if not target_id:
                print("Product not found.")
                failed_entries += 1
            else:
                success = inventory_entry.update_stock(target_id)

                # 3. Check the stored result variable
                if not success:
                    failed_entries += 1
                else:
                    delivery_amount = inventory_entry.process_delivery()

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
            display_goodbye_message()
            break

        case _:
            print("Invalid option. Please try again.")