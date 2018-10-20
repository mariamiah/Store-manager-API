import unittest
from api import app
from flask import json


class TestSaleViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client

    def test_create_a_sale(self):
        # Tests that a sale record is created
        post_data = ({
            "product_name": "Brown shirt",
            "price": "88000",
            "product_quantity": "44"
        })
        response = self.client().post('/api/v1/sales',
                                      content_type='application/json',
                                      data=json.dumps(post_data))
        self.assertEqual(response.status_code, 201)

    def test_fetch_all_sales(self):
        # Tests that the end point fetches no sales if token is not provided
        response = self.client().get('/api/v1/sales',
                                     content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_fetch_a_single_record(self):
        # Tests that the end point successfully returns a single sale record
        response = self.client().get('/api/v1/sales/1',
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_fetch_one_sale_id(self):
        # Tests that the function returns invalid for wrong indices
        response = self.client().get('/api/v1/sales/0',
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
