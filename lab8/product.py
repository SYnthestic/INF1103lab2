class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = 0
        self.update_stock(stock)

    @property
    def product_id(self): return self.__product_id
    @property
    def name(self): return self.__name
    @property
    def price(self): return self.__price
    @property
    def stock(self): return self.__stock

    def update_stock(self, quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("Quantity must be a whole number.")
        if not 0 <= quantity <= 500:
            raise ValueError("Quantity must be between 0 and 500.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(
            f"ID: {self.product_id} | "
            f"Name: {self.name} | "
            f"Price: ${self.price:.2f} | "
            f"Stock: {self.stock}"
        )

    @staticmethod
    def process_delivery(delivery_amount: float, quantity_inp: int) -> float:
        qty = int(quantity_inp)
        delivery = float(delivery_amount)

        if qty > 0:
            delivery += qty
            print(f"Delivery amount updated to: {delivery}")
            return delivery  
        else:
            print("No delivery amount added for zero or negative entries.")
            return delivery


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
