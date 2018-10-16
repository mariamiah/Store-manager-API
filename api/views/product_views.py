from flask import Blueprint, jsonify, request, make_response
from api.models.product_model import Product
from api.validators import check_empty_fields
from datetime import datetime

product = Blueprint('product', __name__)

products = []


@product.route('/api/v1/products', methods=['POST'])
def create_product():
    """Creates a new product"""
    data = request.get_json()
    validate = check_empty_fields(data)
    try:
        if validate == "Valid":
            product_id = len(products)
            product_id += 1
            date_added = datetime.now()
            date_modified = datetime.now()
            new_product = Product(product_id, data['product_name'],
                                  data['price'], data['product_quantity'],
                                  date_added, date_modified)
            products.append(new_product)
            return jsonify({"message": "Product successfully created"}), 201
        return make_response(validate)
    except ValueError:
        return jsonify({"message": "Invalid fields"}), 400
