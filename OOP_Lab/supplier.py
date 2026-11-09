class Supplier:
    def __init__(self, supplier_id, name, contact_email):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_email = contact_email

    def display_information(self) -> None:
        base_info = super().get_information_string()
        print(base_info + f"Supplier ID: {self.supplier_id} \nSupplier Name: {self.name} \nContact Info: {self.contact_email}")
