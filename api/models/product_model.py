from database_handler import DbConn
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

    def compute_stock_balance(self, product_quantity, product_name):
        """Checks for product quantity"""
        sql = """ SELECT product_quantity FROM products
                  WHERE product_name = '{}'"""
        self.cur.execute(sql.format(product_name))
        row = self.cur.fetchone()
        quantity = row[0]
        if quantity >= int(product_quantity):
            return True
        return False

    def fetch_product_price(self, product_name):
        """ Returns the price of a given product"""
        sql = """ SELECT price FROM products WHERE product_name = '{}'"""
        try:
            self.cur.execute(sql.format(product_name))
            row = self.cur.fetchone()
            return row[0]
        except Exception:
            return False

    def reduce_stock_after_sale(self, product_quantity, product_name):
        """ Reduces stock quantity after a sale is done """
        sql = """ SELECT product_quantity FROM products
                  WHERE product_name = '{}'"""
        self.cur.execute(sql.format(product_name))
        row = self.cur.fetchone()
        new_quantity = row[0] - int(product_quantity)
        sql = """UPDATE products SET product_quantity = '{}'\
                 WHERE product_name = '{}'"""
        self.cur.execute(sql.format(new_quantity, product_name))
