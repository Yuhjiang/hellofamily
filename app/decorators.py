from functools import wraps
from flask import abort
from flask_login import current_user
from .models.permission import Permission


def permission_required(permission):
    """
    验证权限的装饰器
    FOLLOW 1, COMMENT 2, WRITE 4, MODERATE 8, ADMIN 16
    :param permission: 需验证权限
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)
