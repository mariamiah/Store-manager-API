from database_handler import DbConn
import psycopg2
from flask import jsonify, request


class Product:
    """This class defines the product sold by the store"""
    def __init__(self):
        self.product_id = 0
        self.product_quantity = ""
        self.price = ""
        self.product_code = ""
        self.product_name = ""
        conn = DbConn()
        self.cur = conn.create_connection()

    def add_new_product(self, product_quantity, price, product_code,
                        product_name):
        self.product_quantity = product_quantity
        self.price = price
        self.product_code = product_code
        self.product_name = product_name
        sql = """INSERT INTO products(product_quantity, price, product_code, product_name)
                            VALUES ('{product_quantity}', '{price}',
                                    '{product_code}', '{product_name}')"""
        sql_command = sql.format(product_quantity=self.product_quantity,
                                 price=self.price,
                                 product_code=self.product_code,
                                 product_name=self.product_name)
        self.cur.execute(sql_command)

    def check_if_product_exists(self, product_name):
        """ Checks if the product exists"""
        sql = """SELECT product_name from products"""
        self.cur.execute(sql)
        row = self.cur.fetchall()
        for value in row:
            if value[0] == product_name:
                return True
            return False

if __name__ == "__main__":
    product = Product()
