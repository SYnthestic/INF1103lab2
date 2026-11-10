from orderline import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str):
        self.order_id: str = order_id
        # COMPOSITION: The Order directly owns and manages the lifecycle of these OrderLine items.
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Creates an OrderLine inside the Order, establishing Composition."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        """Calculates the total cost of the order by summing the subtotals of each OrderLine."""
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def remove_order_line(self, product_id: str) -> bool:
        """Finds and removes an OrderLine by its product ID."""
        for line in self.order_lines:
            if line.product.product_id == product_id:
                self.order_lines.remove(line)
                return True
        return False
