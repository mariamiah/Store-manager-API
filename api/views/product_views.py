from flask import Blueprint, jsonify, request
from api.models.product_model import Product
from api.models.user_models import User
from api.validators import Validate
from datetime import datetime
from flasgger import swag_from
from api.views.user_views import token_required
from uuid import uuid4

product = Blueprint('product', __name__)

validate = Validate()


@product.route('/api/v2/products', methods=['POST'])
@swag_from('../apidocs/products/create_product.yml')
@token_required
def create_product():
    """Creates a new product"""
    user = User()
    fetched_token = request.headers['Authorization']
    token = fetched_token.split(" ")[1]
    if user.validate_token(token):
        return jsonify({"message": "Token blacklisted, login again"}), 400
    if validate.check_permission(token):
        return jsonify({"message": "Permission Denied, Not Admin"}), 400
    data = request.get_json()
    product = Product()
    product_code = uuid4()
    valid = validate.validate_product(data)
    date_added = datetime.now()
    try:
        if valid == "Valid":
            if product.check_if_product_exists(data['product_name']):
                return jsonify({"message": "Product already exists"})
            product.add_new_product(data['product_quantity'], data['price'],
                                    product_code, data['product_name'],
                                    date_added)
            return jsonify({"message":
                            "Product added successfully"}), 201
        return jsonify({"message": valid}), 400
        created_token.remove(data_token)
    except ValueError:
        return jsonify({"message": "Invalid fields"}), 400


@product.route('/api/v2/products', methods=['GET'])
@swag_from('../apidocs/products/get_products.yml')
def fetch_all_products():
    """Fetches all the available products from the database"""
    product = Product()
    fetched_products = product.fetch_product()
    return jsonify({"Products": fetched_products}), 200


@product.route('/api/v2/products/<int:product_id>', methods=['DELETE'])
@swag_from('../apidocs/products/delete_product.yml')
@token_required
def delete_product(product_id):
    user = User()
    fetched_token = request.headers['Authorization']
    token = fetched_token.split(" ")[1]
    if user.validate_token(token):
        return jsonify({"message": "Token blacklisted, login again"}), 400
    if validate.check_permission(token):
        return jsonify({"message": "Permission Denied, Not Admin"}), 400
    product = Product()
    if product_id == 0 or product.check_if_id_exists(product_id):
        return jsonify({"message": "Index out of range"}), 400
    product.delete_product(product_id)
    return jsonify({"message": "product successfully removed"}), 200


@product.route('/api/v2/products/<int:product_id>', methods=['PUT'])
@swag_from('../apidocs/products/update_product.yml')
@token_required
def modify_product(product_id):
    """Updates a product"""
    user = User()
    fetched_token = request.headers['Authorization']
    token = fetched_token.split(" ")[1]
    if user.validate_token(token):
        return jsonify({"message": "Token blacklisted, login again"}), 400
    if validate.check_permission(token):
        return jsonify({"message": "Permission Denied, Not Admin"}), 400
    product = Product()
    if product_id == 0 or product.check_if_id_exists(product_id):
        return jsonify({"message": "Index is out of range"}), 400
    data = request.get_json()
    valid = validate.validate_product(data)
    if valid == "Valid":
        product.update_product(product_id, data['product_quantity'],
                               data['product_name'], data['price'])
        return jsonify({'message': "successfully updated"}), 200
    return jsonify({"message": valid}), 400
