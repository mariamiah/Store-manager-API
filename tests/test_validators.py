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

    def test_validate_user(self):
        # Tests that the correct user definitions pass
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara",
            "password": "1323443",
            "email": "sarah@gmail.com",
            "role": "Admin"
        }
        self.assertEqual(self.validate.validate_user(user_data), "is_valid")

    def test_if_no_user_added(self):
        # Tests that the function returns none if no user is added
        user_data = {}
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("No user added", 400))

    def test_return_if_employeename_is_blank(self):
        # Tests the value returned if the employeename is left blank
        user_data = {
            "employee_name": "",
            "gender": "female",
            "username": "sara",
            "password": "1323443",
            "email": "sarah@gmail.com",
            "role": "Attendant"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Employee name cannot be blank", 400))

    def test_return_if_username_is_blank(self):
        # Tests the value returned if the username is left blank
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "",
            "password": "1323443",
            "email": "sarah@gmail.com",
            "role": "admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("User name cannot be blank", 400))

    def test_return_if_password_is_blank(self):
        # Tests the value returned if the password is left blank
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara",
            "password": "",
            "email": "sarah@gmail.com",
            "role": "admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Password cannot be blank", 400))

    def test_return_if_email_is_blank(self):
        # Tests the value returned if the email is left blank
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara",
            "password": "475543",
            "email": "",
            "role": "admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Email cannot be blank", 400))

    def test_employee_name_regex(self):
        # Tests that the function only allows alphanumeric characters in the
        # employee_name
        user_data = {
            "employee_name": "sara@@@$%@%@",
            "gender": "female",
            "username": "sara",
            "password": "475543",
            "email": "sara@gmail.com",
            "role": "admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Only alphanumerics allowed in employee name",
                             400))

    def test_user_name_regex(self):
        # Tests that the function only allows alphanumeric characters in the
        # user_name
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara#^#^@&@",
            "password": "475543",
            "email": "sara@gmail.com",
            "role": "admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Only alphanumerics allowed in user name",
                             400))

    def test_password_length(self):
        # Tests the length of the password
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara",
            "password": "47",
            "email": "sara@gmail.com",
            "role": "admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Password too short", 400))

    def test_return_if_wrong_role_entered(self):
        # Tests to ensure that only admin and attendant are acceptable
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara",
            "password": "475677r",
            "email": "sara@gmail.com",
            "role": "Administrat"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Role must be either Admin or Attendant", 400))
