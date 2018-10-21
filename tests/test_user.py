import unittest
from api.models.user_models import User


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.user = User(1, "sarah", "sarah@gmail.com", "female", "sara",
                         "1234567", "admin")

    def test_employee_id(self):
        # Tests that the employee_id is equal to the given id
        self.assertEqual(self.user.employee_id, 1, "employee_id must be 1")
        self.user.employee_id = 2
        self.assertEqual(self.user.employee_id, 2, "employee_id is now 2")

    def test_employee_id_type(self):
        # Tests the datatype of the employee id
        self.assertNotIsInstance(self.user.employee_id, str)
        self.assertIsInstance(self.user.employee_id, int)

    def test_user_email(self):
        # Tests that the email is equal to the given email
        self.assertEqual(self.user.email, "sarah@gmail.com")

    def test_email_type(self):
        # Tests the datatype of the email
        self.assertIsInstance(self.user.email, str)
        self.assertNotIsInstance(self.user.email, int)

    def test_gender_attribute(self):
        # Tests that the gender is equal to the given gender
        self.assertEqual(self.user.gender, "female")

    def test_gender_datatype(self):
        # Tests the gender data type
        self.assertIsInstance(self.user.gender, str)
        self.assertNotIsInstance(self.user.gender, float)
        self.assertNotIsInstance(self.user.gender, int)

    def test_password(self):
        # Tests that the password is equal to the given password
        self.assertEqual(self.user.password, "1234567")
        self.user.password = "56784"
        self.assertEqual(self.user.password, "56784",
                         "password is now 56784")

    def test_role(self):
        # Tests that the role is equal to the given role
        self.assertEqual(self.user.role,
                         'admin')

    def test_class_instance(self):
        # Tests that the defined object is an instance of the User class
        self.assertIsInstance(self.user, User)
