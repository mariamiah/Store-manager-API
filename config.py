class Config(object):
    """
    Common configurations
    """
    SECRET_KEY = 'topsecret'
    DEBUG = False


database_config = {
        "dbname": "storemanagerdb",
        "user": "postgres",
        "password": "123",
        "host": "127.0.0.1",
        "port": "5432"
}

test_database_config = {
        "dbname": "test_storemanagerdb",
        "user": "postgres",
        "password": "123",
        "host": "127.0.0.1",
        "port": "5432"
}
