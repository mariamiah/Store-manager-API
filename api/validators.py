from flask import jsonify, request
import re


def validate_product(data):
    """Validates product fields"""
    try:
        if data['product_name'] == "":
            return jsonify({'message': "Enter product_name"}), 400

        if data['price'] == "":
            return jsonify({"message": "Enter the price of the product"}), 400

        if data["product_quantity"] == "":
            return jsonify({"message": "Enter the product quantity"}), 400

        if not re.match(r"^[a-zA-Z0-9 _]*$", data['product_name']):
            return jsonify({
                "message": "productname should contain alphanumerics only"}),\
                400

        if not re.match(r"^[0-9_]*$", data['price']):
            return jsonify({
                "message": "price should contain integers only"}), 400

        if not re.match(r"^[0-9_]*$", data['product_quantity']):
            return jsonify({
                "message": "quantity should contain integers only"}), 400
        else:
            return "Valid"
    except KeyError:
        return "Invalid Key Fields"
