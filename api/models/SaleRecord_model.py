class SaleRecord:
    def __init__(self, record_id, product_name, price, product_quantity,
                 total_amount, date_added):
        self.record_id = record_id
        self.product_name = product_name
        self.price = price
        self.product_quantity = product_quantity
        self.total_amount = total_amount
        self.date_added = date_added

    def get_dict(self):
        dict = {
            "record_id": self.record_id,
            "product_name": self.product_name,
            "price": self.price,
            "product_quantity": self.product_quantity,
            "total_amount": self.total_amount,
            "date_added": self.date_added
        }
        return dict
