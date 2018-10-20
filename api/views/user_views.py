from flask import request, jsonify, Blueprint, make_response
from api.models.user_models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from api.validators import Validate
from datetime import datetime, timedelta
from functools import wraps
from config import Config
import jwt
import re

user = Blueprint('user', __name__)

users = []


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({"message": "Missing Token"}), 403
        try:
            jwt.decode(token, Config.SECRET_KEY)
        except:
            return jsonify({"message": "Invalid token"}), 403
        return f(*args, **kwargs)
    return decorated


@user.route('/api/v1/users', methods=['POST'])
@swag_from('../apidocs/users/create_user.yml')
def register_user():
    """ registers a user"""
    data = request.get_json()
    validate_user = Validate()
    is_valid = validate_user.validate_user(data)
    for user in users:
        if user.email == data['email']:
            return "user already exists!", 400
    try:
        if is_valid == "is_valid":
            employee_id = len(users)
            employee_id += 1
            hashed_password = generate_password_hash(data['password'],
                                                     method='sha256')
            user = User(employee_id, data['employee_name'], data['email'],
                        data['gender'], data['username'], hashed_password,
                        data['role'])
            users.append(user)
            return jsonify({"message":
                            "User registered successfully"}), 201
        return make_response(is_valid)
    except KeyError:
        return "Invalid key fields"


@user.route('/api/v1/login', methods=['POST'])
@swag_from('../apidocs/users/login_user.yml')
def login():
    """Logs in a user"""
    data = request.get_json()
    validate_data = Validate()
    email = data['email']
    try:
        is_valid = validate_data.validate_login(data)
        if re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email) and\
           is_valid == "Credentials valid":
            return assigns_token(data)
        return make_response(is_valid)
    except KeyError:
        return "Invalid data"


def assigns_token(data):
    for employee in users:
        if employee.email == data['email'] and\
           check_password_hash(employee.password, data['password']):
            if employee.role == 'admin':
                token = jwt.encode({'user': employee.role,
                                    'exp': datetime.utcnow() +
                                    timedelta(minutes=30), 'roles': ["Admin"]},
                                   Config.SECRET_KEY)
                return jsonify({'token': token.decode('UTF-8')}), 200
            if employee.role == 'attendant':
                token = jwt.encode({'user': employee.role,
                                    'exp': datetime.utcnow() +
                                    timedelta(minutes=30),
                                    'roles': ["Attendant"]},
                                   Config.SECRET_KEY)
                return jsonify({'token': token.decode('UTF-8')}), 200
    return jsonify({
        "message": "User either not registered or forgot password"}), 400
