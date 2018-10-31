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
        sql = """SELECT product_name FROM products\
              where product_name = '{}' """
        self.cur.execute(sql.format(product_name))
        row = self.cur.fetchone()
        if row:
            return True
        return False

    def fetch_product(self):
        items = []
        sql = """ SELECT * FROM products"""
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        print(rows)
        for row in rows:
            items.append({
                "product_id": row[0],
                "product_quantity": row[1],
                "price": row[2],
                "product_code": row[3],
                "product_name": row[4]
                })
        return items

    def delete_product(self, product_id):
        sql = """ DELETE FROM products WHERE product_id = '{}'"""
        self.cur.execute(sql.format(product_id))

    def check_if_id_exists(self, product_id):
        """ Checks if id exists"""
        sql = """SELECT * FROM products WHERE product_id ='{}'"""
        self.cur.execute(sql.format(product_id))
        row = self.cur.fetchone()
        if not row:
            return True
        return False

    def update_product(self, product_id, product_quantity,
                       product_name, price):
        """Updates a product"""

        sql = """UPDATE products SET product_quantity='{}',\
                 product_name='{}', price ='{}' WHERE product_id = '{}'"""
        self.cur.execute(sql.format(product_quantity, product_name, price,
                         product_id))

if __name__ == "__main__":
    product = Product()
