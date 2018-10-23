import unittest
from api import app
import json


class TestUserViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_register_a_user(self):
        # Tests that the user is registered
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
        self.assertEqual(response.status_code, 201)
