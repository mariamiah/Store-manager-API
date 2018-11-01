import unittest
from api.models.sale_record_model import SaleRecord


class TestSaleRecord(unittest.TestCase):
    def setUp(self):
        # Creates an instance of the SaleRecord class
        kwargs = {
            "sale_id": 5,
            "product_name": "floral blouse",
            "price": "75000",
            "product_quantity": "20",
            "total_amount": "150000",
            "date_added": "Tue, 16 Oct 2018 18:42:38 GMT"
        }
        self.new_record = SaleRecord(**kwargs)
        return self.new_record

    def test_if_class_is_instance(self):
        # Tests if the object is an instance of the class
        self.assertIsInstance(self.new_record, SaleRecord)

    def test_sale_id(self):
        # Tests that the id is equal to the given id
        self.assertNotEqual(self.new_record.sale_id, 1)
        self.assertNotEqual(self.new_record.sale_id, "str")
        self.assertEqual(self.new_record.sale_id, 5)

    def test_sale_id_data_type(self):
        # Tests the data type of the id
        self.assertNotIsInstance(self.new_record.sale_id, str)
        self.assertNotIsInstance(self.new_record.sale_id, float)
        self.assertIsInstance(self.new_record.sale_id, int)

    def test_sold_product_name(self):
        # Tests the existence of the product name
        self.assertEqual(self.new_record.product_name, "floral blouse")
        self.assertNotEqual(self.new_record.product_name, "skirt")

    def test_sold_product_datatype(self):
        # Tests the datatype of the sold product name
        self.assertNotIsInstance(self.new_record.product_name, int)
        self.assertNotIsInstance(self.new_record.product_name, float)
        self.assertIsInstance(self.new_record.product_name, str)

    def test_sold_product_price(self):
        # Tests the given price
        self.assertEqual(self.new_record.price, "75000")
        self.new_record.price = "50000"
        self.assertEqual(self.new_record.price, "50000",
                         "Price has now changed to 50000")

    def test_sold_product_price_datatype(self):
        # Tests the datatype of the selling price
        self.assertNotIsInstance(self.new_record.price, int)
        self.assertNotIsInstance(self.new_record.price, float)
        self.assertIsInstance(self.new_record.price, str)

    def test_sold_product_quantity(self):
        # Tests that the product_quantity is equal to the given quantity
        self.assertEqual(self.new_record.product_quantity, "20")
        self.assertNotEqual(self.new_record.product_quantity, "23")
        self.assertNotEqual(self.new_record.product_quantity, "32")

    def test_sold_product_quantity_datatype(self):
        # Tests the datatype of the product quantity
        self.assertNotIsInstance(self.new_record.product_quantity, int)
        self.assertNotIsInstance(self.new_record.product_quantity, float)
        self.assertNotIsInstance(self.new_record.product_quantity, list)
        self.assertIsInstance(self.new_record.product_quantity, str)

    def test_total_amount(self):
        # Tests that the total amount is the product of price and quantity
        self.assertEqual(self.new_record.total_amount, "150000")
        self.assertNotEqual(self.new_record.total_amount, "65")

    def test_total_amount_type(self):
        # Tests the datatype of the total amount
        self.assertNotIsInstance(self.new_record.total_amount, int)
        self.assertNotIsInstance(self.new_record.total_amount, float)
        self.assertIsInstance(self.new_record.total_amount, str)

    def test_date_added(self):
        # Tests the date added is equal to the given date
        self.assertNotEqual(self.new_record.date_added, "today")
        self.assertEqual(self.new_record.date_added,
                         "Tue, 16 Oct 2018 18:42:38 GMT")

    def test_date_added_datatype(self):
        # Tests the date type of date added property
        self.assertNotIsInstance(self.new_record.date_added, int)
        self.assertIsInstance(self.new_record.date_added, str)

    def test_get_dict_function_returns_a_dictionary(self):
        # Tests that the function returns a dictionary
            response = {
                    "sale_id": 1,
                    "product_name": "jeans",
                    "price": "5000",
                    "product_quantity": 5,
                    "total_amount": "13000",
                    "date_added": "Tue, 16 Oct 2018 18:42:38 GMT"
               }
            self.assertEqual(response['sale_id'], 1)
            self.assertEqual(response['price'], '5000')
