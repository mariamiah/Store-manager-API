import unittest
from api import app
import json
import jwt
from config import Config


class TestUserViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_register_and_login(self):
        # Tests that the user is registered and logs in as attendant
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara",
            "password": "475677r",
            "email": "sara@gmail.com",
            "role": "Admin"
        }
        response = self.client.post('/api/v1/users',
                                    content_type='application/json',
                                    data=json.dumps(user_data))
        msg = json.loads(response.data)
        self.assertIn("User registered successfully", msg['message'])
        self.assertEqual(response.status_code, 201)
        login_details = {
            "email": "sara@gmail.com",
            "password": "475677r"
        }
        response = self.client.post('/api/v1/login',
                                    content_type='application/json',
                                    data=json.dumps(login_details))
        msg = json.loads(response.data)
        data_token = jwt.decode(msg['token'], Config.SECRET_KEY)
        self.assertIn('Admin', data_token['roles'])

    def test_login_user_if_not_registered(self):
        # Tests that a user cannot log in if wrong details are passed or no
        #  registered
        user_details = {
            "email": "maria@gmail.com",
            "password": "1234"
        }
        response = self.client.post('/api/v1/login',
                                    content_type='application/json',
                                    data=json.dumps(user_details))
        msg = json.loads(response.data)
        self.assertIn("User either not registered or forgot password",
                      msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_exception_raised(self):
        # Tests that a key error is raised for wrong keys
        user_details = {
            "user": "maria@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/login',
                         content_type='application/json',
                         data=json.dumps(user_details))
        self.assertRaises(KeyError)

    def test_user_cant_register_if_already_exists(self):
        # Tests that a user cannot register again if already exists
        user_data = {
            "employee_name": "sarah",
            "gender": "female",
            "username": "sara",
            "password": "475677r",
            "email": "sara@gmail.com",
            "role": "Admin"
        }
        response = self.client.post('/api/v1/users',
                                    content_type='application/json',
                                    data=json.dumps(user_data))
        msg = json.loads(response.data)
        self.assertIn("user already exists!", msg['message'])
        self.assertEqual(response.status_code, 400)
