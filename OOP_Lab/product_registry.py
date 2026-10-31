_PRODUCT_TYPES = {}

def register_product(label: str):
    """Class decorator: makes a product class available to the menu."""
    def wrapper(cls):
        _PRODUCT_TYPES[label] = cls
        return cls
    return wrapper

def get_product_types() -> dict:
    return dict(_PRODUCT_TYPES)