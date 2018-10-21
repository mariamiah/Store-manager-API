class Config(object):
    """
    Common configurations
    """
    SECRET_KEY = 'topsecret'
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True


class TestingConfig(Config):
    """
    Testing application configuration
    """
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
