from product import Product
from product_registry import register_product


@register_product("Subscription")
class SubscriptionProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 duration_months: int):
        super().__init__(product_id, name, price, stock)
        self.duration_months = duration_months

    @property
    def subscription_fee(self) -> float:
        """Price is treated as the monthly fee."""
        return self.price

    @classmethod
    def from_ui(cls, product_id, name, price, stock):
        """Factory method: prompts for the extra field this type needs."""
        while True:
            try:
                duration = int(input("Enter duration in months: ").strip())
                if duration > 0:
                    break
                print("Duration must be greater than 0.")
            except ValueError:
                print("Please enter a whole number.")
        return cls(product_id, name, price, stock, duration)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["duration_months"] = self.duration_months
        return data

    @classmethod
    def from_dict(cls, product_id, details):
        return cls(product_id, details["name"], float(details["price"]),
                   int(details["stock"]), int(details["duration_months"]))

    def display_information(self) -> None:
        base_info = super().get_information_string()
        print(base_info + f" | Fee: ${self.subscription_fee}/month | Duration: {self.duration_months} months")

    def get_fulfilment_info(self) -> str:
        """SubscriptionProduct returns a message with the recurring fee and duration."""
        return (f"Your product is subscribed at a fee of ${self.subscription_fee}/month "
                f"for a duration of {self.duration_months} months")