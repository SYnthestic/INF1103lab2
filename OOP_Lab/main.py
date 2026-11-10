import os

from filehandling import FileHandling
from product_registry import get_product_types
from supplier import Supplier

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

def select_product_class():
    types = list(get_product_types().items())
    print("Select Product Type:")
    for number, (label, _) in enumerate(types, start=1):
        print(f"{number}. {label} Product")

    choice = input(f"Enter choice (1-{len(types)}): ").strip()
    try:
        return types[int(choice) - 1][1]
    except (ValueError, IndexError):
        return None

def get_valid_input(inventory_entry, failed_entries: int):
    # Dynamic ID assignment based on maximum current element suffix to protect against deletion gaps
    if not inventory_entry.inventory:
        next_num = 1
    else:
        next_num = max(int(p.product_id[1:]) for p in inventory_entry.inventory) + 1
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

def get_supplier() -> Supplier:
    while True:
        supplier_id = input("Enter Supplier ID: ").strip()
        supplier_name = input("Enter Supplier Name: ").strip()
        supplier_email = input("Enter Supplier Contact Email: ").strip()
        if supplier_id and supplier_name and supplier_email:
            return Supplier(supplier_id, supplier_name, supplier_email)
        print("Error! Supplier ID, name, and email cannot be blank.\n")

def display_goodbye_message():
    print('''
    Thank you for using Inventory Management System.
    Program terminated.''')



while key != 7:
    keyverify = False
    while keyverify == False:
        print('''
----------- MENU ----------- 
1. Display All Products 
2. Add Product 
3. Update Stock 
4. Search Product 
5. Remove Product
6. Save Inventory 
7. Exit 
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
                inventory_entry.display_all()
                print("-" * 60)
        case 2:
            print("Adding new product...")
            product_id, name, price, stock, failed_entries = get_valid_input(inventory_entry, failed_entries)

            product_class = select_product_class()
            if product_class is None:
                print("Invalid choice.")
                continue

            supplier = get_supplier()

            try:
                new_product = product_class.from_ui(product_id, name, price, stock, supplier)

                delivery_amount, next_id = inventory_entry.add_product(new_product)
                print(new_product.get_fulfilment_info())
                print(f"Total Inventory Shipping Fees: ${inventory_entry.total_shipping_fees():.2f}")

            except (ValueError, TypeError) as validation_err:
                print(f"Insertion Error: {validation_err}")
                failed_entries += 1 

        case 3:
            print("Update Stock")
            target_id = input("Enter Product ID to update stock: ").strip()

            if not target_id:
                print("Product not found.")
                failed_entries += 1
            else:
                success = inventory_entry.update_stock(target_id)
                if not success:
                    failed_entries += 1
                else:
                    delivery_amount = inventory_entry.process_delivery()

        case 4:
            print("Searching Product")
            product_id = input("Enter Product ID: ").strip()
            product = inventory_entry.find_product(product_id)

            if product is None:
                print("Product not found")
                failed_entries = inventory_entry.failed_entries
            else:
                print("Product Found")
                print("-" * 60)
                product.display_information()
                print("-" * 60)

        case 5:
            print("Removing Product")
            if not inventory_entry.inventory:
                print("Inventory is empty.")
                continue

            product_id = input("Enter Product ID to remove: ").strip()
            if not product_id:
                print("Error! Product ID cannot be blank.")
                failed_entries += 1
            else:
                removed = inventory_entry.remove_product(product_id)
                if removed is None:
                    print("Product not found.")
                    failed_entries += 1
                else:
                    delivery_amount = inventory_entry.process_delivery()
                    print(f"Product '{removed.name}' ({removed.product_id}) removed successfully.")

        case 6:
            print("Saving inventory...")
            FileHandling.save_inventory(inventory_entry, delivery_amount, FILE_PATH)

        case 7:
            print("Saving inventory before exit.")
            FileHandling.save_inventory(inventory_entry, delivery_amount, FILE_PATH)
            display_goodbye_message()
            break

        case _:
            print("Invalid option. Please try again.")
