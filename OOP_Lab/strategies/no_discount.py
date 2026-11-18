from .discount_strategy import DiscountStrategy

class NoDiscount(DiscountStrategy):
    """A discount strategy that applies no discount."""
    
    def apply(self, total: float) -> float:
        """Returns the total without any discount."""
        return total