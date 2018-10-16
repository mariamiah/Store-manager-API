from flask import jsonify, request


def check_empty_fields(data):
    """Validates product fields"""
    try:
        if data['product_name'] == "":
            return jsonify({'message': "Enter product_name"}), 400

        if data['price'] == "":
            return jsonify({"message": "Enter the price of the product"}), 400

        if data["product_quantity"] == "":
            return jsonify({"message": "Enter the product quantity"}), 400
        else:
            return "Valid"
    except KeyError:
        return "Missing Fields"
