from inventory import Inventory
from products.digitalproduct import DigitalProduct
from products.physicalproduct import PhysicalProduct
from products.subscriptionproduct import SubscriptionProduct
from supplier import Supplier
from order import Order  # Ensure these match your local filenames/paths
from orderline import OrderLine


# Create a shared default supplier for your initial legacy laboratory test data
default_supplier = Supplier("SUP-00", "Default Depot", "warehouse@depot.com")

inventory = Inventory()  # creating the primary inventory object from the Inventory class

# Create objects from the SUBCLASSES instead of the parent class
product1 = PhysicalProduct("P001", "Laptop", 1200.00, 15, default_supplier, weight=10.0)
print(product1.get_fulfilment_info())

product2 = PhysicalProduct("P002", "Mouse", 25.50, 40, default_supplier, weight=0.20)
inventory.add_product(product1)  # pass the product to inventory class to store in a list
inventory.add_product(product2)

product3 = PhysicalProduct("P004", "Monitor", 299.99, 10, default_supplier, weight=2.88)
inventory.add_product(product3)

# Creating a Physical Product (Adding Weight and Warehouse Location)
product4 = PhysicalProduct("P005", "Gaming Chair", 249.99, 8, default_supplier, weight=18.5)
inventory.add_product(product4)

# Creating a Digital Product (Adding Download Size and File Format)
product5 = DigitalProduct("P006", "E-Book: Python Guide", 14.99, 480, default_supplier, download_size=28.56)
inventory.add_product(product5)

product6 = PhysicalProduct("P007", "Tank", 56000000.0, 8, default_supplier, weight=187295.55)
inventory.add_product(product6)

product7 = PhysicalProduct("P008", "CAC290", 43810.0, 1, default_supplier, weight=29300.0)
inventory.add_product(product7)

print("--- Displaying All Initial Products ---")
inventory.display_all()
print("-" * 60)

# ==========================================
# SUB-TASK: SPECIFIC AGGREGATION & INDEPENDENCE TESTS
# ==========================================

# 1. Create a Supplier object independently
tech_supplier = Supplier("SUP-01", "Global Tech Ltd", "contact@globaltech.com")

# 2. Create Products using that Supplier
laptop = PhysicalProduct("P-101", "Gaming Laptop", 1500.0, 10, tech_supplier, weight=2.5)
ebook = DigitalProduct("D-202", "Python Guide", 25.0, 100, tech_supplier, download_size=399.59)
cloud_plan = SubscriptionProduct("S-303", "Cloud Storage", 9.99, 500, tech_supplier)

# 3. Display supplier information THROUGH each Product
print("--- Supplier Info via Products ---")
print(f"{laptop.name} is supplied by: {laptop.supplier.name}")
print(f"{ebook.name} is supplied by: {ebook.supplier.name}")
print(f"{cloud_plan.name} is supplied by: {cloud_plan.supplier.name}")

# 4. Confirm they are separate objects and can exist independently
print("\n--- Independence Check ---")
print("Are laptop and supplier different objects?", laptop is not tech_supplier)
print("Do laptop and ebook share the exact same supplier object?", laptop.supplier is ebook.supplier)

# Delete the products and prove the Supplier still exists on its own
del laptop, ebook, cloud_plan
print("Supplier still exists after products are deleted:", tech_supplier.name)
print("-" * 60)


# ==========================================
# SUB-TASK: INVENTORY MOVEMENTS & DESTRUCTION CHECK
# ==========================================
print("\n=== STARTING MULTI-INVENTORY AGGREGATION TEST ===")

# • Create a Product before creating or adding it to an Inventory.
standalone_product = PhysicalProduct("P-999", "Standalone Smart Screen", 599.99, 5, tech_supplier, weight=4.2)
print(f"Product created outside containers: {standalone_product.name}")

# • Add the Product to Inventory A.
inventory_a = Inventory()
inventory_a.add_product(standalone_product)
print(f"Added to Inventory A. Size of A: {len(inventory_a.inventory)}")

# • Remove it from Inventory A and confirm that the Product object can still be used.
removed_item = inventory_a.remove_product("P-999")
print(f"Removed from Inventory A. Size of A now: {len(inventory_a.inventory)}")
print(f"Confirming removed item is fully operational: Name: {removed_item.name} | Stock: {removed_item.stock}")

# • Add the same Product object to Inventory B.
inventory_b = Inventory()
inventory_b.add_product(removed_item)
print(f"Added same instance to Inventory B. Size of B: {len(inventory_b.inventory)}")

# • Confirm that removing the Product from an inventory does not remove or destroy the Product itself.
# • Consider what happens if an inventory is emptied. The products should not be conceptually destroyed.
print("\n--- Complete Container Destruction / Empty Check ---")
inventory_b.inventory.clear()  # Empties the container completely
print(f"Inventory B completely cleared out. Total items in B: {len(inventory_b.inventory)}")

# Final proof that standalone_product is untouched by container changes
print("Verification Success! The object still lives independently in memory.")
print(f"Final Data Check -> {standalone_product.get_information_string()}")
print("=== ALL AGGREGATION TESTS COMPLETED SUCCESSFULLY ===")

# ==========================================
# SUB-TASK: SECTION 4.3 COMPOSITION TEST RUN
# ==========================================
print("\n=== STARTING ORDER COMPOSITION TEST ===")

# 1. Create Order #1
order1 = Order("ORD-001")

# 2. Add two or more products to the Order using add_order_line()
# We will use product1 (Laptop) and product2 (Mouse) created earlier in the script
order1.add_order_line(product1, 2)
order1.add_order_line(product2, 5)

# 3. Display each order line and calculate the order total
print(f"--- Invoice details for {order1.order_id} ---")
for line in order1.order_lines:
    line.display_information()
print(f"Order Grand Total: ${order1.calculate_total():.2f}\n")

# 4. Add the same Product (product1) to a different Order (Order #2)
order2 = Order("ORD-002")
order2.add_order_line(product1, 1)  # Adding the same Laptop product instance

print(f"--- Invoice details for {order2.order_id} ---")
for line in order2.order_lines:
    line.display_information()
print(f"Order Grand Total: ${order2.calculate_total():.2f}\n")

# 5. Composition Verification Checks using 'is' and 'id()'
print("--- Object Relationship Verification ---")
line_item_order1 = order1.order_lines[0]  # Order 1's Laptop Line
line_item_order2 = order2.order_lines[0]  # Order 2's Laptop Line

print("Are the two OrderLines distinct object instances?", line_item_order1 is not line_item_order2)
print(f"-> OrderLine 1 ID: {id(line_item_order1)} | OrderLine 2 ID: {id(line_item_order2)}")

print("\nDo both independent OrderLines reference the exact same Product object?", 
      line_item_order1.product is line_item_order2.product)
print(f"-> Referenced Product ID: {id(line_item_order1.product)}")

# 6. Remove an order line or remove the Order to demonstrate lifecycle dependence
print("\n--- Testing Lifecycle Destruction ---")
removed_successfully = order1.remove_order_line("P001")
print(f"Laptop line removed from Order 1? {removed_successfully}")
print(f"Remaining line items in Order 1: {len(order1.order_lines)}")

# Explain why OrderLine cannot be managed independently or transferred:
# An OrderLine cannot be shared because its quantity tracking belongs to a single invoice lifecycle.
# If Order 1 is deleted completely, its lines are wiped from memory, but the Product itself remains untouched in the catalog:
del order1
print("Order 1 deleted from memory.")
print(f"Verification: The raw product '{product1.name}' is unaffected and still exists with a stock of {product1.stock}.")
print("=== ALL COMPOSITION TESTS COMPLETED SUCCESSFULLY ===")