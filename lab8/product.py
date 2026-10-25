import os
import json

class Product:
    def __init__(self, productid, name, price, stock):
        self.__productid = productid
        self.__name = name
        self.__price = price
        self.__stock = stock

    

    


    def process_delivery(delivery_amount, quantity_inp):
        if int(quantity_inp) > 0:
            delivery_amount += int(quantity_inp)
            print(f"Delivery amount updated to: {delivery_amount}")
            return delivery_amount

        else:
            print("No delivery amount added for zero or negative entries.")
            return delivery_amount

    def update_stock(inventory, product_id, delivery_amount, failed_entries):
        if product_id is None:
            return delivery_amount, failed_entries

        name = inventory[product_id]["name"]
        new_quantity = input(f"New Stock Quantity: ").strip()

        if not new_quantity.isdigit() or int(new_quantity) > 500:
            print("Invalid input. Please enter a number between 0 and 500.")
            return delivery_amount, failed_entries + 1

        new_quantity = int(new_quantity)
        old_quantity = inventory[product_id]["quantity"]
        inventory[product_id]["quantity"] = new_quantity
        delivery_amount += new_quantity - old_quantity

        print(f"Stock updated successfully!")
        return delivery_amount, failed_entries


    def calculate_tax(delivery_amount):
        tax_rate = 0.1  # 10% tax rate
        tax_amount = delivery_amount * tax_rate
        print("Tax Amount is: ${}".format(tax_amount))
        return tax_amount


    def save_inventory(inventory, delivery_amount, file_name):
        data = {
            "delivery_amount": delivery_amount,
            "inventory": inventory,
        }

        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Inventory saved successfully to inventory.json")


    

    def goodbye_message():
            print('''
    Thank you for using Inventory Management System.
    Program terminated.''')