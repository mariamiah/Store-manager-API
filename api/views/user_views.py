from flask import request, jsonify, Blueprint
from api.validators import Validate
from api.models.user_models import User
from flasgger import swag_from
from datetime import datetime, timedelta
from functools import wraps
import jwt


user = Blueprint('user', __name__)
user_obj = User()
validate = Validate()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({"message": "Missing Token"}), 403
            jwt.decode(token, os.getenv('SECRET_KEY'))
        return f(*args, **kwargs)
    return decorated


@user.route('/api/v2/auth/signup', methods=['POST'])
@swag_from('../apidocs/users/create_user.yml')
@token_required
def register_user():
    """ registers a user"""
    user = User()
    fetched_token = request.headers['Authorization']
    token = fetched_token.split(" ")[1]
    if user.validate_token(token):
        return jsonify({"message": "Token blacklisted, login again"}), 400
    if validate.check_permission(token):
        return jsonify({"message": "Permission Denied, Not Admin"}), 400
    data = request.get_json()
    is_valid = validate.validate_user(data)
    try:
        if is_valid == "is_valid":
            if user_obj.check_for_existing_user(data['email']):
                return jsonify({"message": "Email already exists, login"})
            user_obj.add_user(data)
            return jsonify({"message":
                            "User registered successfully"}), 201
        return jsonify({"message": is_valid}), 400
    except Exception:
        return jsonify({"message": "Username already exists, login"}), 400


@user.route('/api/v2/auth/login', methods=['POST'])
@swag_from('../apidocs/users/login_user.yml')
def login():
    data = request.get_json()
    try:
        is_valid = validate.validate_login(data)
        if is_valid == "Credentials valid":
            return assigns_token(data)
        return jsonify({"message": is_valid}), 400
    except Exception:
        return jsonify({"message": "Username doesnot exist, register"}), 400


@user.route('/api/v2/auth/logout', methods=['POST'])
@swag_from('../apidocs/users/logout_user.yml')
def logout():
    """Logs out a user"""
    user = User()
    user_token = request.headers['Authorization']
    token = user_token.split(" ")[1]
    if user.blacklist_token(token):
        return jsonify({"message": "log out successful"}), 200


@user.route('/api/v2/users', methods=['GET'])
@swag_from('../apidocs/users/fetch_users.yml')
@token_required
def fetch_users():
    """ Fetches all registered users"""
    user = User()
    fetched_token = request.headers['Authorization']
    token = fetched_token.split(" ")[1]
    if user.validate_token(token):
        return jsonify({"message": "Token blacklisted, login again"}), 400
    if validate.check_permission(token):
        return jsonify({"message": "Permission Denied, Not Admin"}), 400
    all_users = user.fetch_all_users()
    return jsonify({"Users": all_users}), 200


@user.route('/api/v2/users/<int:employee_id>')
@swag_from('../apidocs/users/fetch_single_user.yml')
@token_required
def fetch_single_user(employee_id):
    """ Returns a single user"""
    user = User()
    fetched_token = request.headers['Authorization']
    token = fetched_token.split(" ")[1]
    if user.validate_token(token):
        return jsonify({"message": "Token blacklisted, login again"}), 400
    if validate.check_permission(token):
        return jsonify({"message": "Permission Denied, Not Admin"}), 400
    try:
        if employee_id != 0:
            single_user = user.fetch_single_user(employee_id)
            return jsonify({"Record": single_user}), 200
        return jsonify({"message": "Index out of range!"}), 400
    except Exception:
        return jsonify({"message": "user not found"}), 404


@user.route('/api/v2/users/<int:employee_id>', methods=['PUT'])
@swag_from('../apidocs/users/update_user_role.yml')
@token_required
def update_role(employee_id):
    """Updates the user role"""
    user = User()
    data = request.get_json()
    fetched_token = request.headers['Authorization']
    token = fetched_token.split(" ")[1]
    if user.validate_token(token):
        return jsonify({"message": "Token blacklisted, login again"}), 400
    if validate.check_permission(token):
        return jsonify({"message": "Permission Denied, Not Admin"}), 400
    if employee_id == 0:
        return jsonify({"message": "Index is out of range"}), 400
    if data['role'] != 'Admin' and data['role'] != 'Attendant':
        return jsonify({"message": "role can only be Admin or Attendant"}), 400
    user.update_user_role(data['role'], employee_id)
    return jsonify({'message': "role successfully updated"}), 200


def assigns_token(data):
    user = User()
    if user.fetch_password():
        token = jwt.encode({'user': data['username'],
                            'exp': datetime.utcnow() +
                            timedelta(hours=24),
                            'roles': user.get_role()},
                           os.getenv('SECRET_KEY'))
        return jsonify({'token': token.decode('UTF-8')}), 200
    return jsonify({
        "message": "User either not registered or forgot password"}), 400
