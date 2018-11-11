import unittest
from api import app
import json
from database_handler import DbConn


class TestCategoriesViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.create_users_table()
            conn.delete_default_admin()
            conn.create_default_admin()
            conn.create_categories_table()

    def test_create_a_category_without_token(self):
        # Tests that the category is not created if token is missing
        category_data = ({
            "category_name": "Jackets"
        })
        response = self.client.post("/api/v2/categories",
                                    data=json.dumps(category_data))
        msg = json.loads(response.data)
        self.assertIn("Missing Token", msg['message'])
        self.assertEqual(response.status_code, 403)

    def test_create_a_category(self):
        # Tests that the category is created given correct credentials
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        admin_headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
        category_data = ({
            "category_name": "Jackets"
        })
        response = self.client.post("/api/v2/categories",
                                    headers=admin_headers,
                                    json=category_data)
        msg = json.loads(response.data)
        self.assertIn("Category successfully created", msg['message'])
        self.assertEqual(response.status_code, 201)

    def test_create_a_category_if_already_exists(self):
        # Tests that the category is not created if it exists already
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        admin_headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
        category_data = ({
            "category_name": "Jackets"
        })
        self.client.post("/api/v2/categories",
                         headers=admin_headers,
                         json=category_data)
        response = self.client.post("/api/v2/categories",
                                    headers=admin_headers,
                                    json=category_data)
        msg = json.loads(response.data)
        self.assertIn("Category exists already", msg['message'])
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.drop_tables('categories')
            conn.drop_tables('users')
