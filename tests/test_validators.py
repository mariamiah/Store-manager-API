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
                             ("product_name cannot be blank"))

    def test_empty_product_price(self):
        # Tests to ensure the function fails if price is empty
        data = {
            "product_name": "cabbage",
            "product_quantity": "3",
            "price": ""
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("price cannot be blank"))

    def test_empty_product_quantity(self):
        # Tests the function fails if product quantity is empty
        data = {
            "product_name": "jeans",
            "product_quantity": "",
            "price": "40000"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("product_quantity cannot be blank"))

    def test_product_name_characters(self):
        # Tests the product name doesnot accept non alphanumeric characters
        data = {
            "product_name": "&%^&short##$$#sleeved shirt",
            "product_quantity": "54",
            "price": "40000"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("productname should contain alphanumerics only"))

    def test_price_value(self):
        # Tests the price accepts integers only
        data = {
            "product_name": "shorts",
            "product_quantity": "54",
            "price": "thisisprice"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("price should contain integers only"))

    def test_product_quantity_value(self):
        # Tests the product quantity only accepts integers
        data = {
            "product_name": "shirts",
            "product_quantity": "productquantity",
            "price": "17000"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("quantity should contain integers only"))

    def test_wrong_key_values(self):
        # Tests that the function raises an exception with wrong key value
        data = {
            "product_name": "shirts",
            "%&": "5000",
            "price": "17000"
             }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("Invalid Key Fields"))

    def test_return_if_wrong_number_of_keys_are_entered(self):
        # Tests to ensure a wrong number of key values not entered
        data = {
            "product_name": "shirts",
            "product_quantity": "5000",
            "price": "17000",
            "extra values": "many"
             }
        with app.app_context():
            self.assertEqual(self.validate.validate_product(data),
                             ("Invalid number of key fields"))

    def test_validate_user(self):
        # Tests that the correct user definitions pass
        user_data = {
                "employee_name": "jjdjdjs",
                "email": "dorre@gmail.com",
                "gender": "male",
                "username": "mimimimi",
                "password": "123456789",
                "confirm_password": "123456789",
                "role": "Admin"
                }
        self.assertEqual(self.validate.validate_user(user_data), "is_valid")

    def test_if_no_user_added(self):
        # Tests that the function returns none if no user is added
        user_data = {}
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("No user added"))

    def test_invalid_email_format(self):
        # Tests return value if an email is not in correct format
        user_data = {
            "employee_name": "maria",
            "gender": "female",
            "username": "sara",
            "password": "1323443",
            "confirm_password": "1323443",
            "email": "124wekldsmsa",
            "role": "Attendant"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Invalid email format"))

    def test_wrong_username_format(self):
        user_data = {
            "employee_name": "maria",
            "gender": "female",
            "username": "123444282",
            "password": "1323443",
            "confirm_password": "1323443",
            "email": "maria@gmail.com",
            "role": "Attendant"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("user name cannot contain numbers only"))

    def test_return_if_employeename_is_blank(self):
        # Tests the value returned if the employeename is left blank
        user_data = {
            "employee_name": "",
            "gender": "female",
            "username": "sara",
            "password": "1323443",
            "confirm_password": "1323443",
            "email": "sarah@gmail.com",
            "role": "Attendant"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("employee_name cannot be blank"))

    def test_return_if_username_is_blank(self):
        # Tests the value returned if the username is left blank
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "",
            "password": "1323443",
            "confirm_password": "1323443",
            "email": "sarah@gmail.com",
            "role": "Admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("username cannot be blank"))

    def test_return_if_password_is_blank(self):
        # Tests the value returned if the password is left blank
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara",
            "password": "",
            "confirm_password": "",
            "email": "sarah@gmail.com",
            "role": "admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("password cannot be blank"))

    def test_return_if_email_is_blank(self):
        # Tests the value returned if the email is left blank
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara",
            "password": "475543",
            "confirm_password": "475543",
            "email": "",
            "role": "admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("email cannot be blank"))

    def test_employee_name_regex(self):
        # Tests that the function only allows alphanumeric characters in the
        # employee_name
        user_data = {
            "employee_name": "sara@@@$%@%@",
            "gender": "female",
            "username": "sara",
            "password": "475543",
            "confirm_password": "475543",
            "email": "sara@gmail.com",
            "role": "Admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Only alphanumerics allowed in employee name"))

    def test_user_name_regex(self):
        # Tests that the function only allows alphanumeric characters in the
        # user_name
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara#^#^@&@",
            "password": "475543",
            "confirm_password": "475543",
            "email": "sara@gmail.com",
            "role": "admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Only alphanumerics allowed in user name"))

    def test_password_length(self):
        # Tests the length of the password
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara",
            "password": "47",
            "confirm_password": "47",
            "email": "sara@gmail.com",
            "role": "Admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Password too short"))

    def test_return_if_wrong_role_entered(self):
        # Tests to ensure that only admin and attendant are acceptable
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara",
            "password": "475677r",
            "confirm_password": "475677r",
            "email": "sara@gmail.com",
            "role": "administ"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("Role must be either Admin or Attendant"))

    def test_return_if_wrong_gender_value_entered(self):
        # Tests to ensure that only admin and attendant are acceptable
        user_data = {
            "employee_name": "sarah",
            "gender": "onetwothree",
            "username": "sara",
            "password": "475677r",
            "confirm_password": "475677r",
            "email": "sara@gmail.com",
            "role": "Admin"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_user(user_data),
                             ("gender can only be female or male"))

    def test_return_if_more_keys_entered(self):
        # Tests to ensure that if more than 2 keys is not accepted
        sale_data = {
            "product_quantity": "4",
            "product_name": "blouse",
            "price": "50000",
            "category": "shoes"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_sale(sale_data),
                             ("Invalid keys"))

    def test_return_if_product_name_and_quantity_missing(self):
        # Tests to ensure that if product_name and quantity not provided
        sale_data = {
            "price": "50000",
            "category": "shoes"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_sale(sale_data),
                             ("Add product name and quantity"))

    def test_validate_sales(self):
        # Tests to ensure that correct sales definition passes
        sale_data = {
            "product_quantity": "4",
            "product_name": "blouse"
        }
        with app.app_context():
            self.assertEqual(self.validate.validate_sale(sale_data),
                             ("Sale_valid"))
