from .discount_strategy import DiscountStrategy

class BulkDiscount(DiscountStrategy):
    """A discount strategy that applies a bulk discount.
    Discount rate is applied if total order exceeds 200. It takes 20 off any total of 200 or more."""
    
    def __init__(self, threshold: int, amount: float):
        self.threshold = threshold
        self.amount = amount

    def apply(self, total: float) -> float:
        """Returns the total with the bulk discount applied if the threshold is met."""
        if total >= self.threshold:
            return total - self.amount
        return total