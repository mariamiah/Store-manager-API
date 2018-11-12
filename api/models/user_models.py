from database_handler import DbConn
from flask import jsonify, request
from werkzeug.security import check_password_hash
from config import secret_key
import jwt


class User:
    "A class to describe the User class"

    def __init__(self):
        self.employee_id = 0
        self.employee_name = ""
        self.email = ""
        self.gender = ""
        self.username = ""
        self.password = ""
        self.role = ""
        conn = DbConn()
        self.cur = conn.create_connection()
        conn.create_users_table()
        conn.create_blacklisted_tokens()

    def add_user(self, employee_name, email, gender, username, password, role):
        self.employee_name = employee_name
        self.email = email
        self.gender = gender
        self.username = username
        self.password = password
        self.role = role
        sql = """INSERT INTO users(employee_name, email, gender, username, password, role)
                            VALUES ('{employee_name}', '{email}', '{gender}',
                                    '{username}',
                                    '{password}', '{role}')"""
        sql_command = sql.format(employee_name=self.employee_name,
                                 email=self.email, gender=self.gender,
                                 username=self.username,
                                 password=self.password,
                                 role=self.role)
        self.cur.execute(sql_command)

    def check_for_existing_user(self, email):
        """ Checks if the email is already registered"""
        sql = """SELECT email from users"""
        self.cur.execute(sql)
        row = self.cur.fetchall()
        for value in row:
            if value[0] == email:
                return jsonify({"message": "User already registered, Login"})

    def fetch_password(self):
        data = request.get_json()
        sql = """SELECT password FROM users WHERE username='{}'"""
        self.cur.execute(sql.format(data['username']))
        row = self.cur.fetchone()
        if check_password_hash(row[0], data['password']):
            return True
        return False

    def get_role(self):
        data = request.get_json()
        sql = """SELECT role FROM users WHERE username = '{}'"""
        self.cur.execute(sql.format(data['username']))
        role = self.cur.fetchone()
        if role:
            return role

    def blacklist_token(self, token):
        sql = """INSERT INTO blacklisted(token) VALUES ('{}')"""
        self.cur.execute(sql.format(token))
        return True

    def validate_token(self, token):
        """ Checks if token exists in blacklist database"""
        sql = """SELECT token FROM blacklisted WHERE token = '{}'"""
        self.cur.execute(sql.format(token))
        row = self.cur.fetchone()
        if row:
            return True
        return False

    def fetch_current_user(self):
        """ Fetches the current user"""
        token = request.headers['Authorization']
        data_token = token.split(" ")[1]
        decoded_token = jwt.decode(data_token, secret_key)
        current_user = decoded_token['user']
        return current_user

    def fetch_all_users(self):
        """ Fetches all registered users in the system"""
        users = []
        sql = """ SELECT * FROM users"""
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            users.append(
                {
                    "employee_id": row[0],
                    "employee_name": row[1],
                    "email": row[2],
                    "gender": row[3],
                    "username": row[4],
                    "password": row[5],
                    "role": row[6]
                }
            )
        return users

    def fetch_single_user(self, employee_id):
        """Fetches a single user"""
        specific_user = []
        sql = """SELECT * FROM users WHERE employee_id = '{}'"""
        self.cur.execute(sql.format(employee_id))
        row = self.cur.fetchone()
        specific_user.append({
            "employee_id": row[0],
            "employee_name": row[1],
            "email": row[2],
            "gender": row[3],
            "username": row[4],
            "password": row[5],
            "role": row[6]
        })
        return specific_user

    def update_user_role(self, new_role, employee_id):
        """Updates the user role"""
        sql = """UPDATE users SET role ='{}' WHERE employee_id = '{}'"""
        self.cur.execute(sql.format(new_role, employee_id))
