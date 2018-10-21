import unittest
from api import app
from flask import json


class TestSaleViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client

    def test_fetch_all_sales(self):
        # Tests that the end point fetches no sales if token is not provided
        response = self.client().get('/api/v1/sales',
                                     content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_fetch_one_sale_id(self):
        # Tests that the function returns invalid for wrong indices
        response = self.client().get('/api/v1/sales/0',
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
