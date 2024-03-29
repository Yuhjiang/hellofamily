from .. import db
from .. import login_manager
from .role import Role
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask import current_app, url_for
from .permission import Permission
from .topic import Topic
from .comment import Comment
from .follow import Follow


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    icon = db.Column(db.String(128), default='/static/images/helloproject.ico')
    topics = db.relationship('Topic', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='comment_author', lazy='dynamic')
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('followers', lazy='joined'),
                               lazy='dynamic', cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 用户角色赋予
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User {}: {}>'.format(self.id, self.username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """
        生成token，并和user.id绑定
        :param expiration: 有效时间
        :return: 处理后的字符串
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        """
        根据token激活相关用户
        :param token: generate_confirmation_token生成的含有user.id的token值
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_password(self, expiration=3600):
        """
        生成重置密码需要的token
        :param expiration: 有效时间
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        """
        解析token，重置密码
        :param token:
        :param new_password:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if User is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        """
        生成修改邮箱的token，保存user_id，new_email
        :param new_email: 新邮箱
        :param expiration: 有效时间
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'change_email': self.id, 'new_email': new_email}).deocde('utf-8')

    def change_email(self, token):
        """
        解析token，重置邮箱
        :param token:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            # 邮箱已存在
            return False
        self.email = new_email
        db.session.add(new_email)
        return True

    def can(self, perm):
        """
        用户权限判断
        :param perm: 权限
        :return:
        """
        return self.role is not None and self.role.has_permissions(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        """
        更新用户状态，上次访问时间
        :return:
        """
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def follow(self, user):
        """
        关注某人
        :param user: 被关注的人
        """
        if not self.is_following(user):
            f = Follow(follower_id=self.id, followed_id=user.id)
            db.session.add(f)

    def unfollow(self, user):
        """
        取消关注某人
        :param user: 取消关注的人
        :return:
        """
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        """
        是否关注某人
        :param user:
        :return:
        """
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        """
        是否被某人关注
        :param user:
        :return:
        """
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    def generate_auth_token(self, expiration):
        """
        生成用于REST API身份验证的令牌
        验证基于HTTPAuth
        :param expiration: 过期时间
        :return: 令牌
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        """
        验证REST API身份验证的令牌是否有效
        :param token: 令牌，包含了user.id
        :return: 从令牌里提取出的用户数据
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_json(self) -> dict:
        """
        适用于REST API的dict格式的user数据，返回数据后会在路由中jsonify处理
        :return:字典格式的user数据
        """
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'topics_url': url_for('api.get_user_topics', id=self.id),
            'followed_topics_url': url_for('api.get_user_followed_topics', id=self.id),
            'topic_count': self.topics.count()
        }
        return json_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
