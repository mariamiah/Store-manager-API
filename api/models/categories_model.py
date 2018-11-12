from database_handler import DbConn


class Category:
    """This class defines the categories for the different
       products in the store"""
    def __init__(self):
        self.category_id = 0
        self.category_name = ""
        self.created_at = ""
        conn = DbConn()
        self.cur = conn.create_connection()
        conn.delete_default_admin()
        conn.create_default_admin()
        conn.create_categories_table()

    def add_new_category(self, category_name, created_at):
        self.category_name = category_name
        self.created_at = created_at
        sql = """INSERT INTO categories(category_name, created_at)
                            VALUES ('{category_name}', '{created_at}')"""
        sql_command = sql.format(category_name=self.category_name,
                                 created_at=self.created_at)
        self.cur.execute(sql_command)

    def check_if_category_exists(self, category_name):
        """checks if category exists"""
        sql = """SELECT * FROM categories WHERE category_name = '{}'"""
        self.cur.execute(sql.format(category_name))
        row = self.cur.fetchone()
        if row:
            return True
        return False
