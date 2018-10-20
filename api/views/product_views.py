from flask import Blueprint, jsonify, request, make_response
from api.models.product_model import Product
from api.validators import Validate
from datetime import datetime
from flasgger import swag_from
from api.views.user_views import token_required


product = Blueprint('product', __name__)

products = []


@product.route('/api/v1/products', methods=['POST'])
@swag_from('../apidocs/products/create_product.yml')
@token_required
def create_product():
    """Creates a new product"""
    data = request.get_json()
    validate = Validate()
    valid = validate.validate_product(data)
    try:
        if valid == "Valid":
            product_id = len(products)
            product_id += 1
            date_added = datetime.now()
            new_product = Product(product_id, data['product_name'],
                                  data['price'], data['product_quantity'],
                                  date_added)
            products.append(new_product)
            return jsonify({"message": "Product successfully created"}), 201
        return make_response(valid)
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
    if product_id != 0 and product_id <= len(products):
        product = products[product_id - 1]
        fetched_product.append(product.serialize())
        return jsonify({"Product": fetched_product}), 200
    return jsonify({"message": "Index out of range!"}), 400
