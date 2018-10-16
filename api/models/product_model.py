class Product:
    """This class defines the product sold by the store"""
    def __init__(self, product_id, product_quantity, price, product_name,
                 date_added):
        self.product_id = product_id
        self.product_quantity = product_quantity
        self.price = price
        self.product_name = product_name
        self.date_added = date_added

    def serialize(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price": self.price,
            "product_quantity": self.product_quantity,
            "date_added": self.date_added,
            }
