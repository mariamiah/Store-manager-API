from flask import Blueprint, jsonify, request
from api.models.SaleRecord_model import SaleRecord
from api.validators import Validate
from datetime import datetime
from api.views.user_views import token_required
from flasgger import swag_from

sale = Blueprint('sale', __name__)

sales = list()
validate = Validate()


@sale.route('/api/v1/sales', methods=['POST'])
@swag_from('../apidocs/sales/create_sale_record.yml')
@token_required
def create_sale_record():
    """ Creates a new sale record"""
    if validate.check_role(created_token):
        return jsonify({"Message": "Permission denied, Not an attendant"}), 401
    data = request.get_json()
    valid = validate.validate_product(data)
    try:
        if valid == "Valid":
            sale_id = len(sales)
            sale_id += 1
            total = int(data['price']) * int(data['product_quantity'])
            date_added = datetime.now()
            kwargs = {
                "sale_id": sale_id,
                "product_name": data['product_name'],
                "price": data['price'],
                "product_quantity": data['product_quantity'],
                "total_amount": str(total),
                "date_added": date_added
            }
            new_record = SaleRecord(**kwargs)
            sales.append(new_record)
            return jsonify({"message": "record created successfully"}), 201
        return jsonify({"message": valid}), 400
    except ValueError:
        return jsonify({"message": "Invalid"})


@sale.route('/api/v1/sales', methods=['GET'])
@swag_from('../apidocs/sales/get_all_sales.yml')
def fetch_sale_orders():
    """This endpoint fetches all sale records"""
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
