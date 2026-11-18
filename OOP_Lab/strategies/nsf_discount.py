from .percentage_discount import PercentageDiscount

class NSFDiscount(PercentageDiscount):
    """Applies 5% off, plus a $5 rebate on orders of $30 or more."""

    def __init__(self, rebate: float = 5.0, min_spend: float = 30.0):
        super().__init__(5)
        self.rebate = rebate
        self.min_spend = min_spend

    def apply(self, total: float) -> float:
        discounted = super().apply(total)

        if total >= self.min_spend:
            discounted -= self.rebate

        return max(0.0, discounted)
