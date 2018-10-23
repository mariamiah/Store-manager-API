import unittest
from api import app
import json


class TestProductViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_create_a_product(self):
        # Tests that the product is not created if token is  not provided
        post_data = ({
            "product_name": "Leather Jacket",
            "price": "50000",
            "product_quantity": "44"
        })
        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=json.dumps(post_data))
        msg = json.loads(response.data)
        self.assertIn("Missing Token", msg['message'])
        self.assertEqual(response.status_code, 403)

    def test_fetch_all_products(self):
        # Tests that the end point fetches all products
        response = self.client.get('/api/v1/products',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_fetch_one_product(self):
        # Tests that the end point does not return the product if not created
        response = self.client.get('/api/v1/products/1',
                                   content_type='application/json')
        msg = json.loads(response.data)
        self.assertIn("Index out of range!", msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_fetch_one_product_id(self):
        # Tests that the function returns invalid for wrong indices
        response = self.client.get('/api/v1/products/0',
                                   content_type='application/json')
        msg = json.loads(response.data)
        self.assertIn("Index out of range!", msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_delete_for_invalid_product_id(self):
        # Tests that the product is not deleted given wrong id
        response = self.client.delete('/api/v1/products/0',
                                      content_type='application/json')
        msg = json.loads(response.data)
        self.assertIn("Index out of range", msg['message'])
        self.assertEqual(response.status_code, 400)
