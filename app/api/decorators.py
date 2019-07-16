"""
用于权限验证的装饰器，为避免和app.decorators已有的功能冲突，
在app.api里重新专用于api的装饰器
"""
from functools import wraps
from .errors import forbidden
from flask import g


def permission_required(permission):
    """
    验证权限的装饰器
    FOLLOW 1, COMMENT 2, WRITE 4, MODERATE 8, ADMIN 16
    """
    def decorate(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permission')
            return f(*args, **kwargs)
        return decorated_function
    return decorate
