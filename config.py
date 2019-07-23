import os
import secret
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    基础环境配置
    """
    SECRET_KEY = secret.secret_key
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = secret.mail_username
    MAIL_PASSWORD = secret.mail_password
    FLASK_MAIL_SUBJECT_PREFIX = '[HelloFamily]'
    FLASK_MAIL_SENDER = secret.mail_username
    FLASK_ADMIN = secret.mail_username              # 管理员账户邮箱
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 100                      # mysql连接池数量
    SQLALCHEMY_POOL_TIMEOUT = 30                    # 数据库任务的过期时间
    CELERY_BROKER_URL = 'redis://localhost'
    CELERY_RESULT_BACKEND = 'redis://localhost'
    FLASK_TOPICS_PER_PAGE = 20                      # 每页显示的文章数量

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
