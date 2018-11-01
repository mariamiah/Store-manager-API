import os
import psycopg2
from config import database_config, test_database_config


class DbConn:
    def create_connection(self):
        """ Function that creates the database based on the application
            environment"""
        if os.environ.get('APP_SETTINGS') == 'testing':
            database_name = "test_storemanagerdb"
        else:
            database_name = "storemanagerdb"

        self.conn = psycopg2.connect(dbname=database_name, user="postgres",
                                     password="123", port="5432",
                                     host="localhost")
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        return self.cur

    def create_users_table(self):
        """A function to create the users table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users
            (employee_id  SERIAL PRIMARY KEY  NOT NULL,
            employee_name VARCHAR(60) NOT NULL,
            email VARCHAR(250) NOT NULL UNIQUE,
            gender VARCHAR(60) NOT NULL,
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            role VARCHAR(100) NOT NULL); ''')

    def create_products_table(self):
        "A function to create the products table"
        self.cur.execute('''CREATE TABLE IF NOT EXISTS products
                     (product_id  SERIAL PRIMARY KEY NOT NULL ,
                      product_quantity INT NOT NULL,
                      price INT NOT NULL,
                      product_code UUID NOT NULL,
                      product_name VARCHAR(100) NOT NULL UNIQUE); ''')

    def create_sales_table(self):
        "A function to create the sales_records table"
        self.cur.execute('''CREATE TABLE IF NOT EXISTS sales_records
                         (sale_id SERIAL PRIMARY KEY NOT NULL,
                          total_amount INT NOT NULL,
                          username VARCHAR(100) REFERENCES users(username) ON\
                          DELETE CASCADE,
                          product_name VARCHAR(100) REFERENCES\
                          products(product_name) ON DELETE CASCADE,
                          product_quantity INT NOT NULL,
                          price INT NOT NULL,
                          date_sold DATE NOT NULL); ''')

    def create_categories_table(self):
        """A function to create the categories table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS categories
                           (category_id  SERIAL PRIMARY KEY   NOT NULL ,
                            category_name VARCHAR(100) NOT NULL,
                            product_id INT REFERENCES products(product_id) ON\
                            DELETE CASCADE ,
                            created_at  DATE); ''')

    def create_blacklisted_tokens(self):
        """Creates a table for the blacklisted tokens """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS blacklisted
                            (token_id SERIAL PRIMARY KEY NOT NULL,
                            token VARCHAR(300) NOT NULL);''')

    def drop_tables(self, table_name):
        """ Drops the tables that exist in the database"""
        sql = """ DROP TABLE {} CASCADE;"""
        self.cur.execute(sql.format(table_name))
        print("Table '{}' successfully dropped".format(table_name))

    def close_DB(self):
        self.conn.commit()
        self.conn.close()
