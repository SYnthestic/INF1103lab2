from canbeshipped import CanBeShipped
from product import Product
from product_registry import register_product


@register_product("Physical")
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

    def to_dict(self) -> dict:
            data = super().to_dict()
            data["weight"] = self.weight
            return data
    
    @classmethod
    def from_dict(cls, product_id, details):
            return cls(product_id, details["name"], float(details["price"]),
                int(details["stock"]), int(details["weight"]))

    def display_information(self) -> None:
        # 1. Get the shared baseline details (ID, Name, Price, Stock)
        base_info = super().get_information_string()
        
        # 2. Calculate this specific item's individual shipping cost
        item_shipping_cost = self.calculate_shipping_cost()
        
        # 3. Print the combined metrics cleanly with correct labels
        print(base_info + f" | Weight: {self.weight:.2f}kg | Shipping Cost: ${item_shipping_cost:.2f}")

    def get_fulfilment_info(self):
            '''PhysicalProduct returns a message explaining that the product requires physical shipping. '''
            return "Your product is delivered physically and requires physical shipping"