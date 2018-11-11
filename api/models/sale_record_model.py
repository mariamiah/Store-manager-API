from database_handler import DbConn


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
                  price, date_sold) VALUES('{}', '{}','{}','{}','{}', '{}')"""
        self.cur.execute(sql.format(total_amount, username, product_name,
                         product_quantity, price, date_sold))

    def view_all_sales(self):
        """ Admin can view all sales"""
        sales = []
        sql = """ SELECT * FROM sales_records"""
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            sales.append({
                "sale_id": row[0],
                "total_amount": row[1],
                "username": row[2],
                "product_name": row[3],
                "product_quantity": row[4],
                "price": row[5],
                "date_sold": row[6]
                })
        return sales

    def view_sale_by_id(self, sale_id):
        """Returns a sale per individual """
        sql = """SELECT * FROM sales_records WHERE sale_id = '{}'"""
        self.cur.execute(sql.format(sale_id))
        row = self.cur.fetchone()
        return {
                "sale_id": row[0],
                "total_amount": row[1],
                "username": row[2],
                "product_name": row[3],
                "product_quantity": row[4],
                "price": row[5],
                "date_sold": row[6]

        }

    def fetch_user_from_sale(self, sale_id):
        """Fetches the user who made a particular sale"""
        sql = """SELECT username FROM sales_records WHERE sale_id = '{}'"""
        self.cur.execute(sql.format(sale_id))
        row = self.cur.fetchone()
        if row:
            return row[0]
        return False

    def check_sale_id_exists(self, sale_id):
        """ Checks if id exists"""
        sql = """SELECT * FROM sales_records WHERE sale_id ='{}'"""
        self.cur.execute(sql.format(sale_id))
        row = self.cur.fetchone()
        if not row:
            return True
        return False
