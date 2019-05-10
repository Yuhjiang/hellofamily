import os
import secret
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    基础环境配置
    """
    SECRET_KEY = secret.secret_key
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True
    MAIL_USERNAME = secret.mail_username
    MAIL_PASSWORD = secret.mail_password
    FLASK_MAIL_SENDER = secret.mail_username
    FLASK_ADMIN = secret.mail_username
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    开发环境配置
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{}@localhost/hfdev'.format(secret.database_password)


class TestConfig(Config):
    """
    测试环境配置
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{}@localhost/hftest'.format(secret.database_password)


class ProductionConfig(Config):
    """
    生产环境配置
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{}@localhost/hellofamily'.format(secret.database_password)


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
