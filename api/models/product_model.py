class Product:
    """This class defines the product sold by the store"""
    def __init__(self, **kwargs):
        self.product_id = kwargs['product_id']
        self.product_quantity = kwargs['product_quantity']
        self.price = kwargs['price']
        self.product_name = kwargs['product_name']
        self.date_added = kwargs['date_added']

    def serialize(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price": self.price,
            "product_quantity": self.product_quantity,
            "date_added": self.date_added,
            }
