import io
import sys
from product import Product

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float): # <-- Added venue_floors
        super().__init__(
            product_id=product_id,
            name=name,
            price=price,
            stock=stock
        )
        self.download_size = download_size # in MB, which is float

    def display_information(self) -> None:
        base_info = super().get_information_string()
        print(base_info + f" | Download size: {self.download_size}MB")