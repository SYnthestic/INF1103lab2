from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        # Direct assignment using the property setter interface safely
        self.stock = stock  

    @property
    def product_id(self): return self.__product_id
    
    @property
    def name(self): return self.__name
    
    @property
    def price(self): return self.__price
    
    @property
    def stock(self):
        # Fallback initializer to guarantee it exists even if accessed early
        if not hasattr(self, '_stock'):
            self._stock = 0
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = value

    # 1. This method builds the raw text and returns it
    def get_information_string(self) -> str:
        return (
            f"ID: {self.product_id} | "
            f"Name: {self.name} | "
            f"Price: ${self.price:.2f} | "
            f"Stock: {self.stock}"
        )

    # 2. This method simply prints whatever the method above returns
    def display_information(self) -> None:
        print(self.get_information_string())

    @abstractmethod
    def get_fulfilment_info():
        pass

    @staticmethod
    def process_delivery(inventory) -> int:
        total = inventory.total_delivery()
        print(f"Delivery amount updated to: {total}")
        return total


    @staticmethod
    def calculate_tax(delivery_amount):
        tax_rate = 0.1  
        tax_amount = delivery_amount * tax_rate
        print(f"Tax Amount is: ${tax_amount:.2f}")
        return tax_amount
    

    @staticmethod
    def goodbye_message():
        print('''
    Thank you for using Inventory Management System.
    Program terminated.''')
