import unittest
import json
from api import app
from config import secret_key
from database_handler import DbConn


class TestUserViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.create_users_table()
            conn.delete_default_admin()
            conn.create_default_admin()
            conn.create_blacklisted_tokens()

    def test_register_user(self):
        # Tests that the user is registered
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
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
                                    headers=headers,
                                    json=user_data)
        msg = json.loads(response.data)
        self.assertIn("User registered successfully", msg['message'])
        self.assertEqual(response.status_code, 201)

    def test_register_with_unmatched_passwords(self):
        # Tests that the user cannot register with un matched passwords
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
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
                                    headers=headers,
                                    json=user_data)
        msg = json.loads(response.data)
        self.assertIn("passwords dont match", msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_configuration(self):
        """ Tests the API configuration key """
        self.assertEqual(secret_key, 'topsecret')

    def test_user_cant_register_if_already_exists(self):
        # Tests that a user cannot register again if already exists
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
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
                                    headers=headers,
                                    json=user_data)
        response = self.client.post('/api/v2/auth/signup',
                                    headers=headers,
                                    json=user_data)
        msg = json.loads(response.data)
        self.assertIn("Email already exists, login", msg['message'])
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """ Tests that a registered user successfully logs in """
        login_details = {
               "username": "Admin",
               "password": "Administrator"
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
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
        response = self.client.post('/api/v2/auth/logout',
                                    headers=headers)
        message = json.loads(response.data)
        self.assertIn("log out successful", message['message'])
        self.assertEqual(response.status_code, 200)

    def test_fetch_all_users(self):
        """Tests the end point that fetches all users"""
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
        users_response = self.client.get('/api/v2/users',
                                         headers=headers)
        msg = json.loads(users_response.data)
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_user(self):
        """ Tests fetch single user end point """
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
        users_response = self.client.get('/api/v2/users/1',
                                         headers=headers)
        msg = json.loads(users_response.data)
        self.assertEqual(response.status_code, 200)

    def test_update_user_role(self):
        """Tests that the admin successfully updates role"""
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
        details = {
            "role": "Admin"
        }
        response = self.client.put('/api/v2/users/1',
                                   headers=headers,
                                   json=details)
        msg = json.loads(response.data)
        self.assertIn("role successfully updated", msg['message'])
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.delete_default_admin()
            conn.drop_tables('users')
            conn.drop_tables('blacklisted')
