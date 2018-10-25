from flask import Blueprint, jsonify, request
from api.models.product_model import Product
from api.validators import Validate
from datetime import datetime
from flasgger import swag_from
from api.views.user_views import token_required, created_token


product = Blueprint('product', __name__)

products = []
validate = Validate()


@product.route('/api/v1/products', methods=['POST'])
@swag_from('../apidocs/products/create_product.yml')
@token_required
def create_product():
    """Creates a new product"""
    if validate.check_role(created_token) is False:
        return jsonify({
            "Message": "Permission denied, Not an admin"}), 401
    data = request.get_json()
    valid = validate.validate_product(data)
    try:
        if valid == "Valid":
            product_id = len(products)
            product_id += 1
            date_added = datetime.now()
            kwargs = {
                'product_id': product_id,
                "product_name": data['product_name'],
                "price": data['price'],
                "product_quantity": data['product_quantity'],
                "date_added": date_added
            }
            new_product = Product(**kwargs)
            products.append(new_product)
            return jsonify({"message": "Product successfully created"}), 201
        return jsonify({"message": valid}), 400
    except ValueError:
        return jsonify({"message": "Invalid fields"}), 400


@product.route('/api/v1/products', methods=['GET'])
@swag_from('../apidocs/products/get_products.yml')
def fetch_products():
    """Fetches all the available products"""
    Products = [product.serialize() for product in products]
    return jsonify({"Products": Products}), 200


@product.route('/api/v1/products/<int:product_id>', methods=['GET'])
@swag_from('../apidocs/products/get_single_product.yml')
def fetch_single_product(product_id):
    fetched_product = []
    try:
        if validate.validate_id(product_id, products):
            product = products[product_id - 1]
            fetched_product.append(product.serialize())
            return jsonify({"Product": fetched_product}), 200
        return jsonify({"message": "Index out of range!"}), 400
    except IndexError:
        return "Index out of range", 400


@product.route('/api/v1/products/<int:product_id>', methods=['DELETE'])
@swag_from('../apidocs/products/delete_product.yml')
def delete_product(product_id):
    if product_id == 0 or product_id > len(products):
        return jsonify({"message": "Index out of range"}), 400
    for product in products:
        if product.product_id == product_id:
            products.remove(product)
    return jsonify({"message": "product successfully removed"}), 200


@product.route('/api/v1/products/<int:product_id>', methods=['PUT'])
@swag_from('../apidocs/products/update_product.yml')
def modify_product(product_id):
    """Updates an entry"""
    if product_id == 0 or product_id > len(products):
        return jsonify({"message": "Index is out of range"}), 400
    data = request.get_json()
    for product in products:
        if int(product.product_id) == int(product_id):
            product.product_name = data['product_name']
            product.product_quantity == data['product_quantity']
            product.price = data['price']
    return jsonify({'message': "successfully updated"}), 200
