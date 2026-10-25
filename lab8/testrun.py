from product import Product
from inventory import Inventory


inventory = Inventory() # creating the inventory object from the Inventory class 
product1 = Product("P001", "Laptop", 1200.00, 15) # creating product from Product class, via init 
product2 = Product("P002", "Mouse", 25.50, 40) 
inventory.add_product(product1) # pass the product to inventory class to store in a list 
inventory.add_product(product2) 