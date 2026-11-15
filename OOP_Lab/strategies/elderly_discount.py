from .percentage_discount import PercentageDiscount

class ElderlyDiscount(PercentageDiscount):
    """Applies 20% off for seniors, or 30% off for Pioneer Generation members."""

    def __init__(self, is_pioneer: bool = False):
        discount_rate = 30 if is_pioneer else 20
        super().__init__(discount_rate)
        self.is_pioneer = is_pioneer

