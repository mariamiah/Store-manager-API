import unittest
from api import app
import json
from database_handler import DbConn


class TestProductViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.create_users_table()
            conn.create_default_admin()
            conn.create_products_table()
            conn.create_blacklisted_tokens()

    def test_create_a_product(self):
        # Tests that the product is not created if token is missing
        post_data = ({
            "product_name": "Leather Jacket",
            "price": "50000",
            "product_quantity": "44"
        })
        response = self.client.post("/api/v2/products",
                                    data=json.dumps(post_data))
        msg = json.loads(response.data)
        self.assertIn("Missing Token", msg['message'])
        self.assertEqual(response.status_code, 403)

    def test_fetch_all_products(self):
        # Tests that the end point fetches all products
        response = self.client.get('/api/v2/products',
                                   content_type='application/json',)
        self.assertEqual(response.status_code, 200)

    def test_post_product_if_admin(self):
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
        product_details = {
                "product_quantity": "6",
                "product_name": "umbrella",
                "price": "3000"
                }
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
        response = self.client.post('/api/v2/products',
                                    headers=headers,
                                    json=product_details)
        msg = json.loads(response.data)
        self.assertIn("Product added successfully", msg['message'])
        self.assertEqual(response.status_code, 201)

    def test_cannot_add_product_if_not_admin(self):
        # Tests that a user cannot add a product if they are not admin
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        user_data = {
                    "employee_name": "ttuehe",
                    "email": "lillian@gmail.com",
                    "gender": "female",
                    "username": "lillian",
                    "password": "123456789",
                    "confirm_password": "123456789",
                    "role": "Attendant"
                }
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
        response = self.client.post('/api/v2/auth/signup',
                                    headers=headers,
                                    json=user_data)
        login_details = {
            "username": "lillian",
            "password": "123456789"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        product_details = {
                "product_quantity": "6",
                "product_name": "umbrella",
                "price": "3000"
                }
        token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = self.client.post('/api/v2/products',
                                    headers=headers,
                                    json=product_details)
        msg = json.loads(response.data)
        self.assertIn("Permission Denied, Not Admin", msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_delete_product_if_admin(self):
        # Tests that an admin can delete a product
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        product_details = {
                "product_quantity": "6",
                "product_name": "umbrella",
                "price": "3000"
                }
        msg = json.loads(response.data)
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
        response = self.client.post('/api/v2/products',
                                    headers=headers,
                                    json=product_details)
        response = self.client.delete('/api/v2/products/1',
                                      headers=headers,
                                      json=product_details)
        message = json.loads(response.data)
        self.assertIn("product successfully removed", message['message'])
        self.assertEqual(response.status_code, 200)

    def test_cannot_delete_if_not_admin(self):
        # Tests that a user can not delete item if not administrator
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        user_data = {
                    "employee_name": "ttuehe",
                    "email": "esther@gmail.com",
                    "gender": "female",
                    "username": "esther",
                    "password": "123456789",
                    "confirm_password": "123456789",
                    "role": "Attendant"
                }
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
        response = self.client.post('/api/v2/auth/signup',
                                    headers=headers,
                                    json=user_data)
        login_details = {
            "username": "esther",
            "password": "123456789"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        product_details = {
                "product_quantity": "6",
                "product_name": "umbrella",
                "price": "3000"
                }
        msg = json.loads(response.data)
        token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = self.client.post('/api/v2/products',
                                    headers=headers,
                                    json=product_details)
        response = self.client.delete('/api/v2/products/1',
                                      headers=headers,
                                      json=product_details)
        message = json.loads(response.data)
        self.assertIn("Permission Denied, Not Admin", message['message'])
        self.assertEqual(response.status_code, 400)

    def test_modify_product_if_admin(self):
        # Tests that its only the administrator who can modify a product
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        product_details = {
                "product_quantity": "6",
                "product_name": "umbrella",
                "price": "3000"
                }
        msg = json.loads(response.data)
        token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + admin_token
        }
        response = self.client.post('/api/v2/products',
                                    headers=headers,
                                    json=product_details)
        response = self.client.put('/api/v2/products/1',
                                   headers=headers,
                                   json=product_details)
        message = json.loads(response.data)
        self.assertIn("successfully updated", message['message'])
        self.assertEqual(response.status_code, 200)

    def test_cannot_modify_product_if_not_admin(self):
        # Tests that a user cannot modify a product if not admin
        login_details = {
               "username": "Admin",
               "password": "Administrator"
            }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        msg = json.loads(response.data)
        admin_token = msg['token']
        user_data = {
                    "employee_name": "ttuehe",
                    "email": "monica@gmail.com",
                    "gender": "female",
                    "username": "monica",
                    "password": "123456789",
                    "confirm_password": "123456789",
                    "role": "Attendant"
                }
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearerer " + admin_token
        }
        response = self.client.post('/api/v2/auth/signup',
                                    headers=headers,
                                    json=user_data)
        login_details = {
            "username": "monica",
            "password": "123456789"
        }
        response = self.client.post('/api/v2/auth/login',
                                    content_type='application/json',
                                    json=login_details)
        product_details = {
                "product_quantity": "6",
                "product_name": "umbrella",
                "price": "3000"
                }
        msg = json.loads(response.data)
        token = msg['token']
        headers = {
            "content_type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = self.client.post('/api/v2/products',
                                    headers=headers,
                                    json=product_details)
        response = self.client.put('/api/v2/products/1',
                                   headers=headers,
                                   json=product_details)
        message = json.loads(response.data)
        self.assertIn("Permission Denied, Not Admin", message['message'])
        self.assertEqual(response.status_code, 400)

    def test_invalid_token_after_logout(self):
        # Tests that one cannot use an invalid token to create a product
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
            "Authorization": "Bearerer " + admin_token
        }
        response = self.client.post('/api/v2/auth/logout',
                                    headers=headers)
        product_details = {
            "product_name": "Teeshirt",
            "price": "100000",
            "product_quantity": "43"
        }
        response = self.client.post('/api/v2/products',
                                    headers=headers,
                                    json=product_details)
        message = json.loads(response.data)
        self.assertIn("Token blacklisted, login again", message['message'])
        self.assertEqual(response.status_code, 400)

    def test_cannot_add_a_product_which_already_exists(self):
        # Tests that a user cannot add an already exisitng product
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
        product_details = {
            "product_name": "Teeshirt",
            "price": "100000",
            "product_quantity": "43"
        }
        response = self.client.post('/api/v2/products',
                                    headers=headers,
                                    json=product_details)
        response = self.client.post('/api/v2/products',
                                    headers=headers,
                                    json=product_details)
        message = json.loads(response.data)
        self.assertIn("Product already exists", message['message'])
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with app.app_context():
            conn = DbConn()
            self.cur = conn.create_connection()
            conn.drop_tables('products')
            conn.drop_tables('blacklisted')
            conn.delete_default_admin()
            conn.drop_tables('users')
