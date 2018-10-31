from database_handler import DbConn
import psycopg2
from flask import jsonify, request
from werkzeug.security import check_password_hash


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

    def logout_user(self, token):
        sql = """INSERT INTO blacklisted(token) VALUES ('{}')"""
        self.cur.execute(sql.format(token))
        
    def token_in_blacklisted(self, token):
        """ Checks if the blacklisted token exists in database"""
        sql = """select token from blacklisted where token ='{}'"""
        self.cur.execute(sql.format(token))
        row = self.cur.fetchone()
        if row:
            return True
        return False

if __name__ == "__main__":
    user = User()
