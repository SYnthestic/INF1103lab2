from .percentage_discount import PercentageDiscount


class DisabilityDiscount(PercentageDiscount):
    """Applies a 50% discount for eligible customers with disabilities."""

    def __init__(self):
        super().__init__(50)


