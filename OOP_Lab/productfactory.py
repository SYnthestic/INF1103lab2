from supplier import Supplier
from product import Product
from product_registry import get_product_types


class ProductFactory:
    @staticmethod
    def _resolve_class(product_type: str):
        classes = {label.lower(): cls for label, cls in get_product_types().items()}
        key = product_type.strip().lower()
        if key not in classes:
            raise ValueError(f"Sorry, no product type: {product_type}, exists.")
        return classes[key]

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, **kwargs) -> Product:
        """Non-interactive creation (CSV loader, tests)."""
        cls = ProductFactory._resolve_class(product_type)
        return cls(product_id, name, price, stock_quantity, supplier, **kwargs)

    @staticmethod
    def create_from_ui(product_type: str, product_id: str, name: str, price: float,
                       stock_quantity: int, supplier: Supplier) -> Product:
        """Interactive creation: the product class prompts for its own extra fields."""
        cls = ProductFactory._resolve_class(product_type)
        return cls.from_ui(product_id, name, price, stock_quantity, supplier)