import io
import sys
from product import Product
class PhysicalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float): # <-- Added venue_floors
        super().__init__(
            product_id=product_id,
            name=name,
            price=price,
            stock=stock
        )
        self.weight = weight #which is in kg, and this is obviously a float because 25kg, 4.46kg, 19000kg are all valid values

    def display_information(self) -> None:
            base_info = super().get_information_string()
            print(base_info + f" | Weight: {self.weight}kg")