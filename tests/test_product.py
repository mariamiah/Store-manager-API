import unittest
from api.models.product_model import Product


class TestProduct(unittest.TestCase):
    def setUp(self):
        kwargs = {
            "product_id": 1,
            "product_quantity": 5,
            "price": 50000,
            "product_name": "Slim Mom Jeans",
            "date_added": "Tue, 16 Oct 2018 18:42:38 GMT"
        }
        self.product = Product(**kwargs)

    def test_product_id(self):
        # Tests that the prodct_id is equal to the given id
        self.assertEqual(self.product.product_id, 1, "product_id must be 1")
        self.product.product_id = 8
        self.assertEqual(self.product.product_id, 8, "product_id is now 8")

    def test_product_id_type(self):
        # Tests the datatype of the product id
        self.assertNotIsInstance(self.product.product_id, str)
        self.assertIsInstance(self.product.product_id, int)

    def test_product_quantity(self):
        # Tests that the product quantity is equal to the given quantity
        self.assertEqual(self.product.product_quantity, 5,
                         "Quantity should be 5")

    def test_product_quantity_type(self):
        # Tests the datatype of the product quantity
        self.assertIsInstance(self.product.product_quantity, int)
        self.assertNotIsInstance(self.product.product_quantity, str)

    def test_product_price(self):
        # Tests that the price is equal to the given product price
        self.assertEqual(self.product.price, 50000, "price must be 50000")

    def test_price_datatype(self):
        # Tests the price of the product
        self.assertIsInstance(self.product.price, int)
        self.assertNotIsInstance(self.product.price, float)
        self.assertNotIsInstance(self.product.price, str)

    def test_product_name(self):
        # Tests that the product name is equal to the given product name
        self.assertEqual(self.product.product_name, "Slim Mom Jeans")
        self.product.product_name = "covert jeans"
        self.assertEqual(self.product.product_name, "covert jeans",
                         "product name is now covert jeans")

    def test_date_added(self):
        # Tests that the date is equal to the given date
        self.assertEqual(self.product.date_added,
                         'Tue, 16 Oct 2018 18:42:38 GMT')

    def test_class_instance(self):
        # Tests that the defined object is an instance of the Product class
        self.assertIsInstance(self.product, Product)

    def test_serialize_function_returns_a_dictionary(self):
        # Tests that the function returns a dictionary
            response = {
                     'product_id': 1,
                     'product_name': 'shirt',
                     'price': '12000',
                     'product_quantity': '10',
                     'date_added': "Tue, 16 Oct 2018 18:42:38 GMT"
               }
            self.assertEqual(response['product_id'], 1)
            self.assertEqual(response['price'], '12000')
