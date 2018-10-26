import unittest
from api import app
import json
from api.validators import Validate
from config import Config


class TestSaleViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_fetch_all_sales(self):
        # Tests that the end point fetches no sales if token is not provided
        response = self.client.get('/api/v1/sales',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_fetch_one_sale_id(self):
        # Tests that the function returns invalid for wrong indices
        response = self.client.get('/api/v1/sales/0',
                                   content_type='application/json')
        msg = json.loads(response.data)
        self.assertIn("Index out of range!", msg['message'])
        self.assertEqual(response.status_code, 400)

    def test_sale_not_created(self):
        # Tests that no sale is created if token is not provided
        response = self.client.post('/api/v1/sales',
                                    content_type='application/json')
        msg = json.loads(response.data)
        self.assertIn("Missing Token", msg['message'])
        self.assertEqual(response.status_code, 403)
