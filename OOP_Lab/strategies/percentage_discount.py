from .discount_strategy import DiscountStrategy

class PercentageDiscount(DiscountStrategy):
    """A discount strategy that applies a percentage discount."""
    
    def __init__(self, percentage: float):
            self.percentage = percentage / 100

    def apply(self, total: float) -> float:
            return total * (1 - self.percentage)