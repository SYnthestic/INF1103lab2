from .discount_strategy import DiscountStrategy

class PercentageDiscount(DiscountStrategy):
    """A discount strategy that applies a percentage discount."""
    
    def __init__(self, amount: float):
        self.discount = 0.9
        self.amount = amount

    def apply(self, total: float) -> float:
        """Returns the total with the bulk discount applied if the threshold is met."""
        return total * self.discount