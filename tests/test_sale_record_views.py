import unittest
from api import app
import json
from database_handler import DbConn
from api.models.sale_record_model import SaleRecord


class TestSaleViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.create_users_table()
            conn.create_default_admin()
            conn.create_products_table()
            conn.create_sales_table()
            conn.create_blacklisted_tokens()

    def test_create_a_sale_without_token(self):
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

    def test_fetch_all_sales_without_token(self):
        # Tests that the end point fetches all sales
        response = self.client.get('/api/v2/sales',
                                   content_type='application/json',)
        self.assertEqual(response.status_code, 403)

    def test_fetch_all_sales_with_token(self):
        # Tests that the end point fetches all sales
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
        response = self.client.get('/api/v2/sales',
                                   headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_fetch_sale_if_admin(self):
        # Tests that a sale is viewed if admin
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
        response = self.client.get('/api/v2/sales',
                                   headers=headers)
        msg = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_post_sale_if_admin(self):
        # Tests that a product is created if admin
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
        sale_details = {
                "product_quantity": "6",
                "product_name": "umbrella"
                }
        response = self.client.post('/api/v2/sales',
                                    headers=headers,
                                    json=sale_details)
        msg = json.loads(response.data)
        self.assertIn("Permission Denied, Not an Attendant", msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_cannot_sale_unexistent_product(self):
        # Tests that cannot add unexistent product
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
                    "email": "jessica@gmail.com",
                    "gender": "female",
                    "username": "jessica",
                    "password": "123456789",
                    "confirm_password": "123456789",
                    "role": "Attendant"
                }
        response = self.client.post('/api/v2/auth/signup',
                                    headers=headers,
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

    def test_views_sale_by_id(self):
        # Tests that an administrator can view a single sale by id
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
                                    headers=admin_headers,
                                    json=user_data)
        login_details = {
            "username": "jessica",
            "password": "123456789"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        product_details = {
            "product_quantity": "3",
            "product_name": "Leather Jacket",
            "price": "5000"
        }
        response = self.client.post('/api/v2/products',
                                    headers=admin_headers,
                                    json=product_details)
        sale_details = {
                "product_quantity": "1",
                "product_name": "Leather Jacket"
                }
        attendant_token = msg['token']
        attendant_headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + attendant_token
        }
        response = self.client.post('/api/v2/sales',
                                    headers=attendant_headers,
                                    json=sale_details)
        response = self.client.get('/api/v2/sales/1',
                                   headers=admin_headers)
        msg = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_return_if_sale_id_exists(self):
        """ Tests the value returned if sale id exists """
        salerecord = SaleRecord()
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
                    "email": "jessica@gmail.com",
                    "gender": "female",
                    "username": "jessica",
                    "password": "123456789",
                    "confirm_password": "123456789",
                    "role": "Attendant"
                }
        response = self.client.post('/api/v2/auth/signup',
                                    headers=headers,
                                    json=user_data)
        login_details = {
            "username": "jessica",
            "password": "123456789"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        product_details = {
                "product_quantity": "1",
                "product_name": "Leather Jacket",
                "price": "120000"
        }
        self.client.post('/api/v2/products',
                         headers=headers,
                         json=product_details)
        sale_details = {
                "product_quantity": "1",
                "product_name": "Leather Jacket"
                }
        attendant_token = msg['token']
        attendant_headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + attendant_token
        }
        self.client.post('/api/v2/sales',
                         headers=attendant_headers,
                         json=sale_details)
        self.assertEqual(salerecord.check_sale_id_exists(1), False)
        self.assertEqual(salerecord.check_sale_id_exists(3), True)

    def tearDown(self):
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.drop_tables('sales_records')
            conn.drop_tables('products')
            conn.delete_default_admin()
            conn.drop_tables('users')
