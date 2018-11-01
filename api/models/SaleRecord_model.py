from database_handler import DbConn
import psycopg2
from flask import jsonify, request
from datetime import datetime


class SaleRecord:
    """This class defines the sales made by the store"""
    def __init__(self):
        self.sale_id = 0
        self.total_amount = ""
        self.username = ""
        self.product_id = ""
        self.date_sold = ""
        conn = DbConn()
        self.cur = conn.create_connection()

    def make_a_sale(self, total_amount, username, product_name,
                    product_quantity, price, date_sold):
        """Adds a sale record"""
        sql = """INSERT INTO sales_records\
                 (total_amount, username, product_name, product_quantity,
                  price, date_sold) VALUES('{}', '{}','{}','{}','{}')"""
        self.cur.execute(sql.format(total_amount, username, product_name,
                         product_quantity, price, date_sold))
        
    def view_all_sales(self):
        """ Admin can view all sales"""
        pass

    def view_sale_by_id(self):
        """Returns a sale per individual """
        pass

    def fetch_product_by_id():
        pass
