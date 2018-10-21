from flask import jsonify, request
import re


class Validate:
    """This class contains validators for the different entries"""

    def validate_product(self, data):
        # Validates the product fields
        try:
            if data['product_name'] == "":
                return "Enter Product name", 400

            if data['price'] == "":
                return "Enter the price of the product", 400

            if data["product_quantity"] == "":
                return "Enter the product quantity", 400

            if not re.match(r"^[a-zA-Z0-9 _]*$", data['product_name']):
                return "productname should contain alphanumerics only", 400

            if not re.match(r"^[0-9_]*$", data['price']):
                return "price should contain integers only", 400

            if not re.match(r"^[0-9_]*$", data['product_quantity']):
                return "quantity should contain integers only", 400
            else:
                return "Valid"
        except KeyError:
            return "Invalid Key Fields"

    def validate_user(self, data):
        # Validates user fields
        try:
            if len(data.keys()) == 0:
                return "No user added", 400

            if data['username'] == "":
                return "User name cannot be blank", 400

            if data['email'] == "":
                return "Email cannot be blank", 400

            if data['password'] == "":
                return "Password cannot be blank", 400

            if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)",
                            data['email']):
                return "Invalid email format", 400

            if not re.match(r"([a-zA-Z ]*$)", data['employee_name']):
                return "Only alphanumerics allowed in employee name", 400

            if not re.match(r"([a-zA-Z0-9]*$)", data['username']):
                return "Only alphanumerics allowed in user name", 400

            if re.match(r"([0-9])", data['username']):
                return "user name cannot contain numbers only", 400

            if len(data['password']) < 5:
                return "Password too short", 400

            if data['role'] != 'admin' and data['role'] != 'attendant':
                return "Role must be either admin or attendant", 400

            if data['employee_name'] == "":
                return "Employee name cannot be blank", 400
            else:
                return "is_valid"
        except KeyError:
            return "Invalid, Key fields missing", 400

    def validate_login(self, data):
        try:
            if len(data.keys()) == 0 or len(data.keys()) > 2:
                return "Only email and password for login", 400

            if 'email' not in data.keys():
                return "Email is missing", 400

            if 'password' not in data.keys():
                return "Missing password", 400
            else:
                return "Credentials valid"
        except KeyError:
            return "Invalid fields"

    def validate_id(self, id, item_list):
        if id != 0 and id <= len(item_list):
            return True
        return False

    def check_role(self, created_token):
        try:
            if created_token[0]['roles'] != 'Attendant':
                return True
            return False
        except IndexError:
            return "Index out of range"
