import re
import jwt
from config import Config


class Validate:
    """This class contains validators for the different inputs"""

    def validate_product(self, data):
        # Validates the product fields
        product_fields = ['product_name', 'product_quantity', 'price']
        try:
            for product_field in product_fields:
                if data[product_field] == "":
                    return product_field + " cannot be blank"

            if len(data.keys()) == 0 or len(data.keys()) > 3:
                return "Invalid key fields"
            if not re.match(r"^[a-zA-Z0-9 _]*$", data['product_name']):
                return "productname should contain alphanumerics only"

            if not re.match(r"^[0-9_]*$", data['price']):
                return "price should contain integers only"

            if not re.match(r"^[0-9_]*$", data['product_quantity']):
                return "quantity should contain integers only"
            else:
                return "Valid"
        except KeyError:
            return "Invalid Key Fields"

    def validate_user(self, data):
        # Validates user fields
        user_fields = ['username', 'email', 'password', 'employee_name',
                       'role', 'gender']
        try:
            if len(data.keys()) == 0:
                return "No user added"
            for user_field in user_fields:
                if data[user_field] == "":
                    return user_field + " cannot be blank"

            if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)",
                            data['email']):
                return "Invalid email format"

            if not re.match(r"([a-zA-Z ]*$)", data['employee_name']):
                return "Only alphanumerics allowed in employee name"

            if not re.match(r"([a-zA-Z0-9]*$)", data['username']):
                return "Only alphanumerics allowed in user name"

            if re.match(r"([0-9])", data['username']):
                return "user name cannot contain numbers only"

            if len(data['password']) < 5:
                return "Password too short"
            if data['gender'] != "female" and data['gender'] != "male":
                return "gender can only be female or male"

            if data['role'] != 'Admin' and data['role'] != 'Attendant':
                return "Role must be either Admin or Attendant"
            if data['password'] != data['confirm_password']:
                return "passwords dont match"
            else:
                return "is_valid"
        except KeyError:
            return "Invalid, Key fields missing"

    def validate_login(self, data):
        try:
            if len(data.keys()) == 0 or len(data.keys()) > 2:
                return "Only username and password for login"
            if 'username' not in data.keys():
                return "Username is missing"
            if 'password' not in data.keys():
                return "Missing password"
            if data['username'] == "" or data['password'] == "":
                return "Input username or password"
            else:
                return "Credentials valid"
        except KeyError:
            return "Invalid fields"

    def validate_id(self, item_id, item_list):
        if item_id != 0 and item_id <= len(item_list):
            return True
        return False

    def check_permission(self, token):
        """ Decodes an encoded token"""
        decoded_token = jwt.decode(token, Config.SECRET_KEY)
        if decoded_token['roles'] != ['Admin']:
            return True
        return False
