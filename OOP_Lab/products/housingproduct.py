from product import Product
from product_registry import register_product
from supplier import Supplier


@register_product("Housing")
class HousingProduct(Product):
    type_name = "housing"
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        rental_area: float,
        rental_duration_days: int
    ):
        super().__init__(
            product_id, name, price, stock, supplier=supplier
        )
        #Validate rental area
        if not isinstance(rental_area, (int, float)) or isinstance(rental_area, bool):
            raise TypeError("Rental area must be a number.")

        if rental_area <= 0:
            raise ValueError("Rental area must be greater than 0.")
        #Validate rental duration days
        if not isinstance(rental_duration_days, int) or isinstance(rental_duration_days, bool):
            raise TypeError("Rental duration must be a whole number.")

        if rental_duration_days <= 0:
            raise ValueError("Rental duration must be greater than 0.")

        self.rental_duration_days = rental_duration_days
        self.rental_area = float(rental_area)

    @property
    def rental_fee(self) -> float:
        """Price is treated as the rental fee."""
        return self.price / self.rental_duration_days

    @classmethod
    def from_ui(cls, product_id, name, price, stock, supplier):
        """Factory method: prompts for the extra field this type needs."""
        while True:
            try:
                rental_duration = int(input("Enter rental duration in days: ").strip())
                if rental_duration > 0:
                    break
                print("Duration must be greater than 0.")
            except ValueError:
                print("Please enter a whole number.")
        while True:
            try:
                rental_area = float(input("Enter rental area in square meters: ").strip())
                if rental_area > 0:
                    break
                print("Area must be greater than 0.")
            except ValueError:
                print("Please enter a valid number.")
        return cls(product_id, name, price, stock, supplier, rental_area, rental_duration)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["rental_duration_days"] = self.rental_duration_days
        data["rental_area"] = self.rental_area
        return data

    @classmethod
    def from_dict(cls, product_id, details):
        return cls(product_id, details["name"], float(details["price"]),
                int(details["stock"]), Supplier.from_dict(details.get("supplier")),float(details["rental_area"]),int(details["rental_duration_days"]))

    def display_information(self) -> None:
        base_info = super().get_information_string()

        print(
            base_info +
            f" | Rental Fee: ${self.rental_fee:.3f}/day"
            f" | Duration: {self.rental_duration_days} days"
            f" | Rental Area: {self.rental_area} square meters"
        )

    def get_fulfilment_info(self) -> str:
        """HousingProduct returns a message with the rental fee and duration."""
        return (f"Your property is rented at a fee of ${self.rental_fee:.3f}/day "
                f"for a duration of {self.rental_duration_days} days"
                f" | Rental Area: {self.rental_area} square meters")