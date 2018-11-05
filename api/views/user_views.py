from flask import request, jsonify, Blueprint
from api.validators import Validate
from api.models.user_models import User
from werkzeug.security import generate_password_hash
from flasgger import swag_from
from datetime import datetime, timedelta
from functools import wraps
from config import secret_key
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
            data_token = jwt.decode(token, secret_key)
        return f(*args, **kwargs)
    return decorated


@user.route('/api/v2/auth/signup', methods=['POST'])
@swag_from('../apidocs/users/create_user.yml')
def register_user():
    """ registers a user"""
    data = request.get_json()
    is_valid = validate.validate_user(data)
    hashed_password = generate_password_hash(data['password'], 'sha256')
    try:
        if is_valid == "is_valid":
            if user_obj.check_for_existing_user(data['email']):
                return jsonify({"message": "Email already exists, login"})
            user_obj.add_user(data['employee_name'], data['email'],
                              data['gender'], data['username'],
                              hashed_password, data['role'])
            return jsonify({"message":
                            "User registered successfully"}), 201
        return jsonify({"message": is_valid}), 400
    except Exception:
        return jsonify({"message": "Invalid"}), 400


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


def assigns_token(data):
    user = User()
    if user.fetch_password():
        token = jwt.encode({'user': data['username'],
                            'exp': datetime.utcnow() +
                            timedelta(minutes=30),
                            'roles': user.get_role()},
                           secret_key)
        return jsonify({'token': token.decode('UTF-8')}), 200
    return jsonify({
        "message": "User either not registered or forgot password"}), 400
