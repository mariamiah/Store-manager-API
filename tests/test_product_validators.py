import unittest
from api.validators import Validate
from api import app


class TestValidator(unittest.TestCase):
    """ Tests Product validators """

    def setUp(self):
        """Sets up the validator class """
        self.validate = Validate()

    def test_validate_product(self):
        # Tests to ensure the correct data definition passes
        data = {
            "product_name": "foods",
            "product_quantity": "4",
            "price": "5000",
        }
        self.assertEqual(self.validate.validate_product(data), "Valid")

    def test_empty_product_name(self):
        # Tests to ensure the function fails if product name is empty
        data = {
            "product_name": "",
            "product_quantity": "3",
            "price": "5000"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("Enter Product name", 400))

    def test_empty_product_price(self):
        # Tests to ensure the function fails if price is empty
        data = {
            "product_name": "mimi",
            "product_quantity": "3",
            "price": ""
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("Enter the price of the product", 400))

    def test_empty_product_quantity(self):
        # Tests the function fails if product quantity is empty
        data = {
            "product_name": "mimi",
            "product_quantity": "",
            "price": "40000"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("Enter the product quantity", 400))

    def test_product_name_characters(self):
        # Tests the product name doesnot accept non alphanumeric characters
        data = {
            "product_name": "maria****",
            "product_quantity": "54",
            "price": "40000"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("productname should contain alphanumerics only",
                             400))

    def test_price_value(self):
        # Tests the price accepts integers only
        data = {
            "product_name": "maria",
            "product_quantity": "54",
            "price": "price"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("price should contain integers only", 400))

    def test_product_quantity_value(self):
        # Tests the product quantity only accepts integers
        data = {
            "product_name": "maria",
            "product_quantity": "quantity",
            "price": "17000"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("quantity should contain integers only", 400))

    def test_wrong_key_values(self):
        # Tests that the function raises an exception with wrong key value
        data = {
            "": "maria",
            "product_quantity": "5000",
            "price": "17000"
             }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("Invalid Key Fields"))
