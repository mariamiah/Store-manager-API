from database_handler import DbConn
import psycopg2
from flask import jsonify, request


class SaleRecord:
    """This class defines the sales made by the store"""
    def __init__(self):
        self._id = 0
        self.total_amount = ""
        self.employee_email = ""
        self.product_code = ""
        self.date_sold = ""
        conn = DbConn()
        self.cur = conn.create_connection()

    def add_sale_record(self):
        """Adds a sale record"""
        pass
