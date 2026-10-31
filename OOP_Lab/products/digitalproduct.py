from product import Product
from product_registry import register_product


@register_product("Digital")
class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float): 
        super().__init__(
            product_id=product_id,
            name=name,
            price=price,
            stock=stock
        )
        self.download_size = download_size # in MB, which is float

    @classmethod
    def from_ui(cls, product_id, name, price, stock):
        """OOP Factory Method: Solves the missing argument by gathering it polymorphically."""
        size_input = input("Enter download size (MB): ").strip()
        download_size = float(size_input) if size_input else 0.0
        return cls(product_id, name, price, stock, download_size)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["download_size"] = self.download_size
        return data

    @classmethod
    def from_dict(cls, product_id, details):
        return cls(product_id, details["name"], float(details["price"]),
                   int(details["stock"]), int(details["download_size"]))

    def display_information(self) -> None:
        base_info = super().get_information_string()
        print(base_info + f" | Download size: {self.download_size}MB")

    def get_fulfilment_info(self):
        '''DigitalProduct returns a message explaining that the product is delivered digitally. '''
        return "Your product is delivered digitally"