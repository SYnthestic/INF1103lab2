from supplier import Supplier
from product import Product

from products.physicalproduct import PhysicalProduct
from products.digitalproduct import DigitalProduct
from products.subscriptionproduct import SubscriptionProduct
from products.housingproduct import HousingProduct

class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, **kwargs) -> Product:
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, **kwargs)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, **kwargs)
        elif product_type == "subscription":
            return SubscriptionProduct(product_id, name, price, stock_quantity, supplier, **kwargs)
        elif product_type == "housing":
            return HousingProduct(product_id, name, price, stock_quantity, supplier, **kwargs)
        else:
            raise ValueError(f"Sorry, no product type: {product_type}, exists.")