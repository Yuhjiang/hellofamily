from flask_httpauth import HTTPBasicAuth
from ..models.user import User
from flask import g, jsonify
from .errors import unauthorized, forbidden
from . import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    print(email_or_token, password)
    if email_or_token == '':
        return False
    if password == '':
        # 检查是否有令牌
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    # 常规密码认证
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return None
    g.current_user = user
    g.token_used = False
    print(123, user.verify_password(password))
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@api.route('/tokens/', methods=['POST'])
def get_token():
    # g.token_used为了避免用户绕过令牌过期机制，使用旧令牌请求新令牌
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})

