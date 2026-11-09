
from inventory import Inventory
from products.digitalproduct import DigitalProduct
from products.physicalproduct import PhysicalProduct
from products.subscriptionproduct import SubscriptionProduct
from supplier import Supplier

inventory = Inventory() # creating the inventory object from the Inventory class 
# 3. Create the object from the SUBCLASS instead of the parent class
product1 = PhysicalProduct("P001", "Laptop", 1200.00, 15, 10) 
print(product1.get_fulfilment_info())
product2 = PhysicalProduct("P002", "Mouse", 25.50, 40, 0.20) 
inventory.add_product(product1) # pass the product to inventory class to store in a list 
inventory.add_product(product2) 
product3 = PhysicalProduct("P004", "Monitor", 299.99, 10, 2.88) # Lab 6 test run object
inventory.add_product(product3)
# Creating a Physical Product (Adding Weight and Warehouse Location)
product4 = PhysicalProduct("P005", "Gaming Chair", 249.99, 8, weight=18.5)
inventory.add_product(product4)
# Creating a Digital Product (Adding Download Size and File Format)
product5 = DigitalProduct("P006", "E-Book: Python Guide", 14.99, 480, download_size=28.56)
inventory.add_product(product5)
product6 = PhysicalProduct("P007", "Tank", 56000000, 8, 187295.55)
inventory.add_product(product6)
product7 = PhysicalProduct("P008", "CAC290", 43810, 1, weight=29300)


inventory.add_product(product7)
inventory.display_all()

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
# Verify they are distinct objects in memory, while sharing the same supplier reference
print("Are laptop and supplier different objects?", laptop is not tech_supplier)
print("Do laptop and ebook share the exact same supplier object?", laptop.supplier is ebook.supplier)

# Delete the products and prove the Supplier still exists on its own
del laptop, ebook, cloud_plan
print("Supplier still exists after products are deleted:", tech_supplier.name)