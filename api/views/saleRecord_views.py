from flask import Blueprint, jsonify, request, make_response
from api.models.SaleRecord_model import SaleRecord
from api.validators import Validate
from datetime import datetime
from api.views.user_views import token_required, created_token
from flasgger import swag_from

sale = Blueprint('sale', __name__)

sales = list()


@sale.route('/api/v1/sales', methods=['POST'])
@swag_from('../apidocs/sales/create_sale_record.yml')
def create_sale_record():
    """ Creates a new sale record"""
    if created_token['token']['roles'] != 'Attendant':
        return jsonify({"Message": "Permission denied, Not an attendant"}), 401
    data = request.get_json()
    validate = Validate()
    valid = validate.validate_product(data)
    try:
        if valid == "Valid":
            record_id = len(sales)
            record_id += 1
            total = int(data['price']) * int(data['product_quantity'])
            date_added = datetime.now()
            new_record = SaleRecord(record_id, data['product_name'],
                                    data['price'],
                                    data['product_quantity'],
                                    str(total), date_added)
            sales.append(new_record)
            return jsonify({"message": "record created successfully"}), 201
        return jsonify({"message": "Invalid fields"}), 400
    except ValueError:
        return jsonify({"message": "Invalid"})


@sale.route('/api/v1/sales', methods=['GET'])
@swag_from('../apidocs/sales/get_all_sales.yml')
@token_required
def fetch_sale_orders():
    """This endpoint fetches all sale records"""
    if created_token['token']['roles'] != 'Admin':
        return jsonify({"Message": "Permission denied, Not an admin"}), 401
    Sales = [record.get_dict() for record in sales]
    return jsonify({"All Sales": Sales}), 200


@sale.route('/api/v1/sales/<int:sale_id>', methods=['GET'])
@swag_from('../apidocs/sales/get_single_sale.yml')
def get_single_record(sale_id):
    single_record = []
    if sale_id != 0 and sale_id <= len(sales):
        record = sales[sale_id - 1]
        single_record.append(record.get_dict())
        return jsonify({"Record": single_record}), 200
    return jsonify({"message": "Index out of range!"}), 400
