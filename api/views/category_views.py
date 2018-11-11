from flask import Blueprint, jsonify, request
from api.models.categories_model import Category
from datetime import datetime
from flasgger import swag_from
from api.validators import Validate
from api.models.user_models import User
from api.views.user_views import token_required

category = Blueprint('category', __name__)
new_category = Category()

validate = Validate()


@category.route('/api/v2/categories', methods=['POST'])
@swag_from('../apidocs/categories/create_category.yml')
@token_required
def create_category():
    """Creates a new category"""
    user = User()
    fetched_token = request.headers['Authorization']
    token = fetched_token.split(" ")[1]
    if user.validate_token(token):
        return jsonify({"message": "Token blacklisted, login again"}), 400
    if validate.check_permission(token):
        return jsonify({"message": "Permission Denied, Not Admin"}), 400
    data = request.get_json()
    category_valid = validate.validate_category(data)
    created_at = datetime.now()
    try:
        if category_valid == "category_valid":
            new_category.add_new_category(data['category_name'], created_at)
            return jsonify({"message":
                            "Category successfully created"}), 201
        else:
            return jsonify({"message": category_valid}), 400
    except Exception:
        return jsonify({"message": " Category exists already"}), 400
