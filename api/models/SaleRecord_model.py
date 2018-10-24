class SaleRecord:
    def __init__(self, **kwargs):
        self.sale_id = kwargs['sale_id']
        self.product_name = kwargs['product_name']
        self.price = kwargs['price']
        self.product_quantity = kwargs['product_quantity']
        self.total_amount = kwargs['total_amount']
        self.date_added = kwargs['date_added']

    def get_dict(self):
        return {
            "sale_id": self.sale_id,
            "product_name": self.product_name,
            "price": self.price,
            "product_quantity": self.product_quantity,
            "total_amount": self.total_amount,
            "date_added": self.date_added
        }
