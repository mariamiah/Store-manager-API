from flask import Blueprint, jsonify, request, make_response
from api.models.SaleRecord_model import SaleRecord
from api.validators import Validate
from datetime import datetime

sale = Blueprint('sale', __name__)

sales = list()


@sale.route('/api/v1/sales', methods=['POST'])
def create_sale_record():
    """ Creates a new sale record"""
    data = request.get_json()
    validate = Validate(data)
    valid = validate.validate_product()
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
