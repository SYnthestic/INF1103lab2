import io
import sys
from product import Product
from canbeshipped import CanBeShipped
class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self.weight = weight

    #Calculates the shipping cost
    def calculate_shipping_cost(self):
        self.calculated_shipping_cost = self.weight * 1.01 + 3
        return self.calculated_shipping_cost

    @classmethod
    def from_ui(cls, product_id, name, price, stock):
        """OOP Factory Method: Solves the missing argument by gathering it polymorphically."""
        size_input = input("Enter weight (in kg): ").strip()
        weight = float(size_input) if size_input else 0.0
        return cls(product_id, name, price, stock, weight)

    def display_information(self) -> None:
        base_info = super().get_information_string()
        print(base_info + f" | Weight: {self.weight}kg")

    def get_fulfilment_info(self):
            '''PhysicalProduct returns a message explaining that the product requires physical shipping. '''
            return "Your product is delivered physically and requires physical shipping"