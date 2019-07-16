"""
1. 初始化flask app
2. 配置app，增加插件
3. 注册路由蓝图
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_moment import Moment
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.chatroom import socketio
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'people.login_or_register'
migrate = Migrate()
admin = Admin(name='hellofamily', template_mode='bootstrap3')


from .models.user import User as Users


class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator()


admin.add_view(UserView(Users, db.session, name='users'))


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])     # 从config类直接导入配置

    # 初始化使用插件后的app
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app)
    moment.init_app(app)
    admin.init_app(app)
    socketio.init_app(app)

    # 注册蓝图
    from .main import main as main_blueprint
    from .user import people as people_blueprint
    from .topic import topic as topic_blueprint
    from .chatroom import chatroom as chatroom_blueprint
    from .api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(people_blueprint, url_prefix='/user')
    app.register_blueprint(topic_blueprint, url_prefix='/topic')
    app.register_blueprint(chatroom_blueprint, url_prefix='/chatroom')
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app

