import unittest
import json
from api import app
from config import Config
from database_handler import DbConn


class TestUserViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.drop_tables('users')
            conn.create_users_table()
            conn.create_blacklisted_tokens()

    def test_register_user(self):
        # Tests that the user is registered
        user_data = {
                    "employee_name": "ttuehe",
                    "email": "sandranaggayi@gmail.com",
                    "gender": "female",
                    "username": "sandra",
                    "password": "123456789",
                    "confirm_password": "123456789",
                    "role": "Admin"
                    }
        response = self.client.post('/api/v2/auth/signup',
                                    content_type='application/json',
                                    json=user_data)
        msg = json.loads(response.data)
        self.assertIn("User registered successfully", msg['message'])
        self.assertEqual(response.status_code, 201)

    def test_register_with_unmatched_passwords(self):
        # Tests that the user is registered
        user_data = {
                    "employee_name": "ttuehe",
                    "email": "sandranaggayi@gmail.com",
                    "gender": "female",
                    "username": "sandra",
                    "password": "123456789",
                    "confirm_password": "abcdefg",
                    "role": "Admin"
                    }
        response = self.client.post('/api/v2/auth/signup',
                                    content_type='application/json',
                                    json=user_data)
        msg = json.loads(response.data)
        self.assertIn("passwords dont match", msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_configuration(self):
        """ Tests the API configuration key """
        self.assertEqual(Config.SECRET_KEY, 'topsecret')

    def tearDown(self):
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.drop_tables('users')
            conn.create_users_table()
            conn.create_blacklisted_tokens()

    def test_user_cant_register_if_already_exists(self):
        # Tests that a user cannot register again if already exists
        user_data = {
                    "employee_name": "ttuehe",
                    "email": "sandranaggayi@gmail.com",
                    "gender": "female",
                    "username": "sandra",
                    "password": "123456789",
                    "confirm_password": "123456789",
                    "role": "Admin"
                }
        response = self.client.post('/api/v2/auth/signup',
                                    content_type='application/json',
                                    json=user_data)
        response = self.client.post('/api/v2/auth/signup',
                                    content_type='application/json',
                                    json=user_data)
        msg = json.loads(response.data)
        self.assertIn("Email already exists, login", msg['message'])
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """ Tests that a registered user successfully logs in """
        user_data = {
                    "employee_name": "ttuehe",
                    "email": "sandranaggayi@gmail.com",
                    "gender": "female",
                    "username": "sandra",
                    "password": "123456789",
                    "confirm_password": "123456789",
                    "role": "Admin"
                }
        response = self.client.post('/api/v2/auth/signup',
                                    content_type='application/json',
                                    json=user_data)
        login_details = {
            "username": "sandra",
            "password": "123456789"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        self.assertEqual(response.status_code, 200)

    def test_login_user_if_not_registered(self):
        # Tests that a user cannot log in if wrong details are passed or no
        #  registered
        user_details = {
            "username": "deborah",
            "password": "12345687"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=user_details)
        msg = json.loads(response.data)
        self.assertIn("Username doesnot exist",
                      msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_cannot_login_if_username_key_not_provided(self):
        # Tests that a user cannot login if username key is missing
        user_details = {
            "": "deborah",
            "password": "12345687"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=user_details)
        msg = json.loads(response.data)
        self.assertIn("Username is missing",
                      msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_cannot_login_if_password_key_not_provided(self):
        # Tests that a user cannot login if username key is missing
        user_details = {
            "username": "deborah",
            "": "12345687"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=user_details)
        msg = json.loads(response.data)
        self.assertIn("Missing password",
                      msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_cannot_login_if_excess_keys(self):
        # Tests that a user cannot login if excess keys are given
        user_details = {
            "username": "deborah",
            "password": "12345687",
            "email": "maria@gmail.com"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=user_details)
        msg = json.loads(response.data)
        self.assertIn("Only username and password for login",
                      msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_cannot_login_if_no_value_for_username_or_password(self):
        user_details = {
            "username": "",
            "password": ""
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=user_details)
        msg = json.loads(response.data)
        self.assertIn("Input username or password",
                      msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_logout_user(self):
        # Tests that a user successfully logs out
        user_data = {
                    "employee_name": "ttuehe",
                    "email": "monica@gmail.com",
                    "gender": "female",
                    "username": "monica",
                    "password": "123456789",
                    "confirm_password": "123456789",
                    "role": "Attendant"
                }
        response = self.client.post('/api/v2/auth/signup',
                                    content_type='application/json',
                                    json=user_data)
        login_details = {
            "username": "monica",
            "password": "123456789"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = self.client.post('/api/v2/auth/logout',
                                    headers=headers)
        message = json.loads(response.data)
        self.assertIn("log out successful", message['message'])
        self.assertEqual(response.status_code, 200)

    def test_assigns_token(self):
        # Tests that a user cannot obtain a token if not logged in
        user_data = {
                    "employee_name": "ttuehe",
                    "email": "monica@gmail.com",
                    "gender": "female",
                    "username": "monica",
                    "password": "123456789",
                    "confirm_password": "123456789",
                    "role": "Attendant"
                }
        response = self.client.post('/api/v2/auth/signup',
                                    content_type='application/json',
                                    json=user_data)
        login_details = {
            "username": "monica",
            "password": "123456789"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        login_details = {
            "username": "monica",
            "password": "monica"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        self.assertIn("User either not registered or forgot password",
                      msg['message'])
        self.assertEqual(response.status_code, 400)
