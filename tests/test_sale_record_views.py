import unittest
from api import app
import json
from database_handler import DbConn


class TestSaleViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.create_sales_table()
            conn.create_products_table()
            conn.create_blacklisted_tokens()

    def test_create_a_sale(self):
        # Tests that the sale is not created if token is missing
        post_data = ({
            "product_quantity": "1",
            "product_name": "shorts"
        })
        response = self.client.post("/api/v2/sales",
                                    data=json.dumps(post_data))
        msg = json.loads(response.data)
        self.assertIn("Missing Token", msg['message'])
        self.assertEqual(response.status_code, 403)

    def test_fetch_all_sales(self):
        # Tests that the end point fetches all sales
        response = self.client.get('/api/v2/sales',
                                   content_type='application/json',)
        self.assertEqual(response.status_code, 403)

    def test_post_sale_if_admin(self):
        # Tests that a product is created if admin
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
        msg = json.loads(response.data)
        sale_details = {
                "product_quantity": "6",
                "product_name": "umbrella"
                }
        token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = self.client.post('/api/v2/sales',
                                    headers=headers,
                                    json=sale_details)
        msg = json.loads(response.data)
        self.assertIn("Permission Denied, Not an Attendant", msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_cannot_sale_unexistent_product(self):
        # Tests that cannot add unexistent product
        user_data = {
                    "employee_name": "ttuehe",
                    "email": "jessica@gmail.com",
                    "gender": "female",
                    "username": "jessica",
                    "password": "123456789",
                    "confirm_password": "123456789",
                    "role": "Attendant"
                }
        response = self.client.post('/api/v2/auth/signup',
                                    content_type='application/json',
                                    json=user_data)
        login_details = {
            "username": "jessica",
            "password": "123456789"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        sale_details = {
                "product_quantity": "1",
                "product_name": "Leather Jacket"
                }
        token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = self.client.post('/api/v2/sales',
                                    headers=headers,
                                    json=sale_details)
        msg = json.loads(response.data)
        self.assertIn("Product does not exist", msg['message'])
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.drop_tables('sales_records')
