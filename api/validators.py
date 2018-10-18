from flask import jsonify, request
import re


class Validate:
    """This class contains validators for the different entries"""
    def validate_product(self, data):
        # Validates the product fields
        try:
            if data['product_name'] == "":
                return "Enter Product name", 400

            if data['price'] == "":
                return "Enter the price of the product", 400

            if data["product_quantity"] == "":
                return "Enter the product quantity", 400

            if not re.match(r"^[a-zA-Z0-9 _]*$", data['product_name']):
                return "productname should contain alphanumerics only", 400

            if not re.match(r"^[0-9_]*$", data['price']):
                return "price should contain integers only", 400

            if not re.match(r"^[0-9_]*$", data['product_quantity']):
                return "quantity should contain integers only", 400
            else:
                return "Valid"
        except KeyError:
            return "Invalid Key Fields"
