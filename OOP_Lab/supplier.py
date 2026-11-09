class Supplier:
    def __init__(self, supplier_id, name, contact_email):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_email = contact_email

    def display_information(self) -> None:
        base_info = super().get_information_string()
        print(base_info + f"Supplier ID: {self.supplier_id} \nSupplier Name: {self.name} \nContact Info: {self.contact_email}")
        
    def to_dict(self) -> dict:
        return {"supplier_id": self.supplier_id, "name": self.name, "contact_email": self.contact_email}

    @classmethod
    def from_dict(cls, details: dict | None) -> "Supplier":
        if not details:
            return cls("UNKNOWN", "Unknown Supplier", "N/A")
        return cls(details["supplier_id"], details["name"], details.get("contact_email", "N/A"))
