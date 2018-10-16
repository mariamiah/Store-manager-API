from flask import jsonify, request
import re


class Validate:
    """This class contains validators for the different entries"""
    def __init__(self, data):
        self.data = data

    def validate_product(self):
        # Validates the product fields
        try:
            if self.data['product_name'] == "":
                return jsonify({'message': "Enter product_name"}), 400

            if self.data['price'] == "":
                return jsonify({
                    "message": "Enter the price of the product"}), 400

            if self.data["product_quantity"] == "":
                return jsonify({
                    "message": "Enter the product quantity"}), 400

            if not re.match(r"^[a-zA-Z0-9 _]*$", self.data['product_name']):
                return jsonify({
                    "message":
                    "productname should contain alphanumerics only"}), 400

            if not re.match(r"^[0-9_]*$", self.data['price']):
                return jsonify({
                    "message": "price should contain integers only"}), 400

            if not re.match(r"^[0-9_]*$", self.data['product_quantity']):
                return jsonify({
                    "message": "quantity should contain integers only"}), 400
            else:
                return "Valid"
        except KeyError:
            return "Invalid Key Fields"
