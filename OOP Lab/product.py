from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.stock = stock  

    @property
    def product_id(self): return self.__product_id
    
    @property
    def name(self): return self.__name
    
    @property
    def price(self): return self.__price
    
    @property
    def stock(self):
        if not hasattr(self, '_stock'):
            self._stock = 0
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = value

    def get_information_string(self) -> str:
        return (
            f"ID: {self.product_id} | "
            f"Name: {self.name} | "
            f"Price: ${self.price:.2f} | "
            f"Stock: {self.stock}"
        )

    def display_information(self) -> None:
        print(self.get_information_string())

    @abstractmethod
    def get_fulfilment_info():
        pass
