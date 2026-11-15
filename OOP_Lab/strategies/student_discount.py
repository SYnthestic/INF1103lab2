from .percentage_discount import PercentageDiscount

class StudentDiscount(PercentageDiscount):
    """Applies a 15% NSF discount, plus an extra $5 rebate
    on orders of $50 or more."""

    def __init__(self, rebate: float = 15.0, min_spend: float = 50.0):
        super().__init__(0.15)

        self.rebate = rebate
        self.min_spend = min_spend

    def apply(self, total: float) -> float:
        discounted = super().apply(total)

        if total >= self.min_spend:
            discounted -= self.rebate

        return max(0.0, discounted)
