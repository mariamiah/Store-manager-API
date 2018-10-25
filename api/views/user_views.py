from flask import request, jsonify, Blueprint
from api.validators import Validate
from api.models.user_models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from datetime import datetime, timedelta
from functools import wraps
from config import Config
import jwt
import re

user = Blueprint('user', __name__)

users = []
created_token = []
validate = Validate()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({"message": "Missing Token"}), 403
        try:
            data_token = jwt.decode(token, Config.SECRET_KEY)
            created_token.append(data_token)
        except:
            return jsonify({"message": "Invalid token"}), 403
        return f(*args, **kwargs)
    return decorated


@user.route('/api/v1/users', methods=['POST'])
@swag_from('../apidocs/users/create_user.yml')
def register_user():
    """ registers a user"""
    data = request.get_json()
    is_valid = validate.validate_user(data)
    for user in users:
        if user.email == data['email']:
            return jsonify({"message": "user already exists!"}), 400
    try:
        if is_valid == "is_valid":
            employee_id = len(users)
            employee_id += 1
            hashed_password = generate_password_hash(data['password'],
                                                     method='sha256')
            kwargs = {
                "employee_id": employee_id,
                "employee_name": data['employee_name'],
                "email": data['email'],
                "gender": data['gender'],
                "username": data['username'],
                "password": hashed_password,
                "role": data['role']
            }
            user = User(**kwargs)
            users.append(user)
            return jsonify({"message":
                            "User registered successfully"}), 201
        return jsonify({"message": is_valid}), 400
    except KeyError:
        return "Invalid key fields"


@user.route('/api/v1/login', methods=['POST'])
@swag_from('../apidocs/users/login_user.yml')
def login():
    """Logs in a user"""
    data = request.get_json()
    try:
        email = data['email']
        is_valid = validate.validate_login(data)
        if re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email) or\
           is_valid == "Credentials valid":
            return assigns_token(data)
        return jsonify({"message": is_valid}), 400
    except KeyError:
        return jsonify({"message": "Invalid keys"}), 400


def assigns_token(data):
    for employee in users:
        if employee.email == data['email'] and\
           check_password_hash(employee.password, data['password']):
                token = jwt.encode({'user': employee.username,
                                    'exp': datetime.utcnow() +
                                    timedelta(minutes=30),
                                    'roles': employee.role},
                                   Config.SECRET_KEY)
                return jsonify({'token': token.decode('UTF-8')}), 200
    return jsonify({
        "message": "User either not registered or forgot password"}), 400
