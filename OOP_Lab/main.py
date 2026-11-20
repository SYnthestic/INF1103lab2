import os

from filehandling import FileHandling
from order import Order
from product import Product
from product_registry import get_product_types
from supplier import Supplier

### The discount strategies
from strategies.percentage_discount import PercentageDiscount
from strategies.no_discount import NoDiscount
from strategies.bulk_discount import BulkDiscount
from strategies.student_discount import StudentDiscount
from strategies.elderly_discount import ElderlyDiscount
from strategies.disability_discount import DisabilityDiscount
from strategies.nsf_discount import NSFDiscount

from productfactory import ProductFactory

failed_entries = 0
delivery_amount = 0
key = -1

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "inventory.json")
ORDER_FILE_PATH = os.path.join(BASE_DIR, "orders.json")
CSV_FILE_PATH = os.path.join(BASE_DIR, "products.csv")

repository = FileHandling(FILE_PATH)
inventory_entry, load_status = repository.load_inventory()
orders = FileHandling.load_orders(ORDER_FILE_PATH, inventory_entry)

BULK_THRESHOLD = 200

if load_status == "not_found":
    print("File not found. Starting a fresh inventory.")
elif load_status == "invalid_file":
    print("Saved file could not be read. Starting a fresh inventory.")
else:
    print("Inventory loaded successfully.")


## Helper Functions
def get_positive_float(prompt: str, failed_entries: int) -> tuple[float, int]:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.") 
                continue 
            return value, failed_entries
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")
            failed_entries += 1


def get_valid_stock(prompt: str, failed_entries: int) -> tuple[int, int]:
    while True:
        try:
            value = int(input(prompt).strip())
            if not (0 <= value <= 500):
                raise ValueError
            return value, failed_entries
        except ValueError:
            print("Please enter a valid whole number between 0 and 500.")
            failed_entries += 1


def get_positive_int(prompt: str, max_val: int | None = None) -> int:
    """Reusable helper for positive integer inputs (e.g., order quantities)."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value <= 0:
                print("Please enter a positive whole number greater than zero.")
                continue
            if max_val is not None and value > max_val:
                print(f"Insufficient stock. Only {max_val} available.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid whole number.")


def get_valid_input(inventory_entry, failed_entries: int):
    if not inventory_entry.inventory:
        next_num = 1
    else:
        next_num = max(int(p.product_id[1:]) for p in inventory_entry.inventory) + 1
    product_id = "P" + str(next_num).zfill(3)

    while True:
        name = input("Enter Product Name: ").strip()
        if name:
            break
        print("Error! Product name cannot be blank.\n")
        failed_entries += 1

    price, failed_entries = get_positive_float("Enter Price: ", failed_entries)
    stock, failed_entries = get_valid_stock("Enter Stock Quantity: ", failed_entries)

    return product_id, name, price, stock, failed_entries


def select_product_type() -> str:
    types = [label.lower() for label in get_product_types()]
    print("Select Product Type:")
    for number, label in enumerate(types, start=1):
        print(f"{number}. {label.capitalize()} Product")

    while True:
        choice = input(f"Enter choice (1-{len(types)}): ").strip()
        try:
            index = int(choice)
            if 1 <= index <= len(types):
                return types[index - 1]
            print(f"Please enter a number between 1 and {len(types)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_supplier() -> Supplier:
    while True:
        supplier_id = input("Enter Supplier ID: ").strip()
        supplier_name = input("Enter Supplier Name: ").strip()
        supplier_email = input("Enter Supplier Contact Email: ").strip()
        if supplier_id and supplier_name and supplier_email:
            return Supplier(supplier_id, supplier_name, supplier_email)
        print("Error! Supplier ID, name, and email cannot be blank.\n")


def show_product_details(product: Product) -> None:
    """Polymorphically prints a product's shared catalog information
    followed by its specific subclass fulfillment details.
    """
    product.display_information()
    print(product.get_fulfilment_info())


def display_goodbye_message():
    print('''
    Thank you for using Inventory Management System.
    Program terminated.''')


def create_customer_order(inventory_entry, order_counter: int) -> Order:
    order_id = "ORD-" + str(order_counter).zfill(3)
    order = Order(order_id)

    while True:
        prod_id = input(
            "Enter Product ID to add to order (or 'done' to finish): "
        ).strip()

        if prod_id.lower() == "done":
            break

        product = inventory_entry.find_product(prod_id)

        if product is None:
            print("Product not found in inventory.")
            continue
        elif product.stock == 0:
            print(f"Product '{product.name}' is out of stock.")
            continue

        # Converted to use get_positive_int helper
        qty = get_positive_int(
            f"Enter quantity for {product.name} (Available: {product.stock}): ",
            max_val=product.stock
        )

        order.add_order_line(product, qty)
        product.stock -= qty
        print(f"Added {qty} x {product.name} to {order.order_id}.")

    if order.order_lines:
        discount_strategy = select_discount_strategy(order)
        order.set_discount(discount_strategy)
        print(f"\nDiscount applied: {type(discount_strategy).__name__}")

    print("\n" + "=" * 60)
    print(f"ORDER SUMMARY: {order.order_id}")
    order.display_summary()
    return order




def select_discount_strategy(order: Order):
    """Lets the customer pick a discount, offering only those the order qualifies for."""
    subtotal = sum(line.calculate_subtotal() for line in order.order_lines)
    # (label, factory, minimum subtotal required)
    all_options = [
        ("No Discount", lambda: NoDiscount(), 0),
        (f"Bulk Discount ($20 off orders of ${BULK_THRESHOLD} or more)",
         lambda: BulkDiscount(BULK_THRESHOLD, 20), BULK_THRESHOLD),
        ("Percentage Discount (10%)", lambda: PercentageDiscount(10), 0),
        ("Student Discount", lambda: StudentDiscount(), 0),
        ("Elderly Discount", lambda: ElderlyDiscount(), 0),
        ("Disability Discount", lambda: DisabilityDiscount(), 0),
        ("NSF Discount", lambda: NSFDiscount(), 0),
    ]
    discount_options = [(label, factory) for label, factory, minimum in all_options
                        if subtotal >= minimum]

    print("\n" + "=" * 45)
    print("SELECT DISCOUNT STRATEGY")
    print(f"Order subtotal: ${subtotal:.2f}")
    print("=" * 45)

    for number, (label, _) in enumerate(discount_options, start=1):
        print(f"{number}. {label}")

    while True:
        choice = input(f"Select discount (1-{len(discount_options)}): ").strip()
        try:
            selected = int(choice)
            if 1 <= selected <= len(discount_options):
                _, strategy_factory = discount_options[selected - 1]
                return strategy_factory()
            print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

## Main Menu Loop
while key != 10:
    print('''
----------- MENU ----------- 
0. Show Orders
1. Display All Products 
2. Add Product 
3. Update Stock 
4. Search Product 
5. Remove Product
6. Create Order
7. Update Discount Type
8. Load Products from CSV
9. Save Inventory & Orders
10. Exit 
----------------------------''')
    try:
        key = int(input("Enter option: ").strip())
    except ValueError:
        print("Invalid input. Please enter a menu number (0-10).")
        continue

    match key:
        case 0:
            Order.show_orders(orders)

        case 1:
            if not inventory_entry.inventory:
                print("Inventory is empty.")
            else:
                inventory_entry.display_all_products()
                print("-" * 60)

        case 2:
            print("Adding new product...")
            product_id, name, price, stock, failed_entries = get_valid_input(inventory_entry, failed_entries)

            type_key = select_product_type()
            supplier = get_supplier()

            try:
                new_product = ProductFactory.create_from_ui(
                    type_key, product_id, name, price, stock, supplier
                )
                delivery_amount, next_id = inventory_entry.add_product(new_product)
                print(new_product.get_fulfilment_info())
                print(f"Total Inventory Shipping Fees: ${inventory_entry.total_shipping_fees():.2f}")
            except (ValueError, TypeError) as validation_err:
                print(f"Insertion Error: {validation_err}")
                failed_entries += 1

        case 3:
            print("Update Stock")
            target_id = input("Enter Product ID to update stock: ").strip()
            product = inventory_entry.find_product(target_id)

            if product is None:
                print("Product not found.")
                failed_entries += 1
            else:
                print("Product Found")
                print("-" * 60)
                show_product_details(product)
                print("-" * 60)

                success = inventory_entry.update_stock(product)
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
                failed_entries += 1
            else:
                print("Product Found")
                print("-" * 60)
                show_product_details(product)
                print("-" * 60)
        case 5:
            print("Removing Product")
            if not inventory_entry.inventory:
                print("Inventory is empty.")
                continue

            target_id = input("Enter Product ID to remove: ").strip()
            if not target_id:
                print("Error! Product ID cannot be blank.")
                failed_entries += 1
                continue

            product = inventory_entry.find_product(target_id)
            if product is None:
                print("Product not found.")
                failed_entries += 1
            else:
                inventory_entry.remove_product(product)
                delivery_amount = inventory_entry.process_delivery()
                print(f"Product '{product.name}' ({product.product_id}) removed successfully.")
        case 6:
            if not inventory_entry.inventory:
                print("Inventory is empty. Add products before creating an order.")
            else:
                next_order_num = max((int(o.order_id.split("-")[1]) for o in orders), default=0) + 1
                new_order = create_customer_order(inventory_entry, next_order_num)
                if new_order.order_lines:
                    orders.append(new_order)
        case 7:
            print("Update Discount Type")
            if not orders:
                print("No orders found.")
                continue

            order_id = input("Enter Order ID (e.g. ORD-001): ").strip().upper()
            order = Order.find_by_id(orders, order_id)
            if order is None:
                print("Order not found.")
                failed_entries += 1
                continue

            print(f"Current total: ${order.calculate_total():.2f}")
            new_strategy = select_discount_strategy(order)
            order.set_discount(new_strategy)
            print(f"Discount updated to: {type(new_strategy).__name__}")
            print(f"New total: ${order.calculate_total():.2f}")

        case 8:
            print("Load Products from CSV")
            print("Products in the file will be assigned to the supplier you enter.")
            supplier = get_supplier()
            FileHandling.load_products(CSV_FILE_PATH, inventory_entry, supplier)
            delivery_amount = inventory_entry.process_delivery()
        case 9:
            print("Saving inventory and Orders...")
            FileHandling.save_inventory(inventory_entry, delivery_amount, FILE_PATH)
            FileHandling.save_orders(orders, ORDER_FILE_PATH)
            FileHandling.save_products(CSV_FILE_PATH, inventory_entry)
        case 10:
            print("Saving inventory and orders before exit.")
            FileHandling.save_inventory(inventory_entry, delivery_amount, FILE_PATH)
            FileHandling.save_orders(orders, ORDER_FILE_PATH)
            FileHandling.save_products(CSV_FILE_PATH, inventory_entry)
            display_goodbye_message()
            break
        case _:
            print("Invalid option. Please try again.")
