from product import Product


class OrderLine:
    """Represents a line item in an order, containing a product and its quantity."""

    def __init__(self, product: Product, quantity: int):
        # Input Validation to ensure data integrity
        if quantity <= 0:
            raise ValueError("Ordered quantity must be greater than zero.")

        # Encapsulation matching the Product class style
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.__quantity = value

    def calculate_subtotal(self) -> float:
        """Calculates the subtotal for this specific line item."""
        return self.product.price * self.quantity

    def display_information(self) -> None:
        """Displays formatted text information about the order line."""
        print(
            f"Product ID: {self.product.product_id} | "
            f"Name: {self.product.name} | "
            f"Quantity: {self.quantity} | "
            f"Subtotal: ${self.calculate_subtotal():.2f}"
        )

    def to_dict(self) -> dict:
        return {
            "product_id": self.product.product_id,
            "name": self.product.name,
            "quantity": self.quantity,
            "subtotal": self.calculate_subtotal(),
        }
