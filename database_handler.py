import os
import psycopg2
from config import database_config, test_database_config


class DbConn:
    def create_connection(self):
        """ Function that creates the database based on the application
            environment"""
        try:
            if os.environ.get('APP_SETTINGS') == 'testing':
                self.conn = psycopg2.connect(**test_database_config)
            else:
                self.conn = psycopg2.connect(**database_config)
            self.cur = self.conn.cursor()
        except Exception as err:
            print(err)

    def create_users_table(self):
        """A function to create the users table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users
            (employee_id  SERIAL PRIMARY KEY  NOT NULL,
            employee_name VARCHAR(60) NOT NULL,
            email VARCHAR(60) NOT NULL UNIQUE,
            gender VARCHAR(10) NOT NULL,
            username VARCHAR(25) NOT NULL,
            password VARCHAR(25) NOT NULL,
            admin BOOLEAN NOT NULL); ''')
        print("Table users created successfully")

    def create_products_table(self):
        "A function to create the products table"
        self.cur.execute('''CREATE TABLE IF NOT EXISTS products
                     (product_id  SERIAL PRIMARY KEY    NOT NULL ,
                      product_quantity INT NOT NULL,
                      price INT NOT NULL,
                      product_code UUID NOT NULL UNIQUE,
                      product_name VARCHAR(25) NOT NULL); ''')
        print("Table products created successfully")

    def create_sales_table(self):
        "A function to create the sales_records table"
        self.cur.execute('''CREATE TABLE IF NOT EXISTS sales_records
                     (sale_id SERIAL PRIMARY KEY NOT NULL,
                      total_amount INT NOT NULL,
                      employee_email VARCHAR(60) REFERENCES users(email) ON\
                      DELETE CASCADE,
                      product_code UUID REFERENCES products(product_code) ON\
                      DELETE CASCADE,
                      date_sold DATE NOT NULL); ''')
        print("Table sales_records created successfully")

    def create_categories_table(self):
        "A function to create the categories table"
        self.cur.execute('''CREATE TABLE IF NOT EXISTS categories
                           (category_id  SERIAL PRIMARY KEY   NOT NULL ,
                            category_name VARCHAR(25) NOT NULL,
                            product_id INT REFERENCES products(product_id) ON\
                            DELETE CASCADE ,
                            created_at  DATE); ''')
        print("Table categories created successfully")

    def close_DB(self):
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
        db = DbConn()
        db.create_connection()
        db.create_users_table()
        db.create_products_table()
        db.create_sales_table()
        db.create_categories_table()
        db.close_DB()