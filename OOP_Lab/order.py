from typing import TYPE_CHECKING

from orderline import OrderLine
from product import Product
from strategies.discount_strategy import DiscountStrategy
from strategies.no_discount import NoDiscount

if TYPE_CHECKING:
    from inventory import Inventory



class Order:
    def __init__(self, order_id: str):
        self.order_id: str = order_id
        # Composition: The Order directly owns and manages the lifecycle of these OrderLine items. As such, they are created and destroyed with the Order.
        self.order_lines: list[OrderLine] = []
        self.discount_strategy: DiscountStrategy = NoDiscount()

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Creates or updates an OrderLine inside the Order, establishing Composition."""
        for line in self.order_lines:
            if line.product.product_id == product.product_id:
                line.quantity += quantity
                return
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = sum(
            line.calculate_subtotal()
            for line in self.order_lines
        )

        discounted_total = self.discount_strategy.apply(total)


        return discounted_total

    def set_discount(self, discount_strategy: DiscountStrategy) -> None:
        """Sets the discount strategy for the order."""
        self.discount_strategy = discount_strategy


    def remove_order_line(self, product_id: str) -> bool:
        """Finds and removes an OrderLine by its product ID."""
        for line in self.order_lines:
            if line.product.product_id == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "order_lines": [line.to_dict() for line in self.order_lines],
            "order_total": self.calculate_total(),
        }

    @staticmethod
    def find_by_id(orders: list["Order"], order_id: str) -> "Order | None":
        for order in orders:
            if order.order_id == order_id:
                return order
        return None

    @classmethod
    def from_dict(cls, data: dict, inventory: "Inventory") -> "Order":
        order = cls(data["order_id"])
        for line_data in data.get("order_lines", []):
            product = inventory.find_product(line_data["product_id"])
            if product is not None:
                order.add_order_line(product, line_data["quantity"])
        return order

    def display_summary(self) -> None:
        print("\n" + "=" * 60)
        print(f"ORDER SUMMARY: {self.order_id}")
        print("=" * 60)
        if not self.order_lines:
            print("No items in order.")
        else:
            for line in self.order_lines:
                line.display_information()
            print("-" * 60)
            print(f"Order Total: ${self.calculate_total():.2f}")
        print("=" * 60)

    @staticmethod
    def show_orders(orders: list["Order"]) -> None:
        """Displays all recorded orders and their line items."""
        if not orders:
            print("No orders found.")
            return
        for order in orders:
            order.display_summary()
