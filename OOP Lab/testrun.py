
from inventory import Inventory
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct


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