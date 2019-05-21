from functools import wraps
from flask import abort, request, redirect, flash, url_for
from flask_login import current_user
from .models.permission import Permission
from .models.comment import Comment
from .models.topic import Topic


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


def comment_delete(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            comment_id = request.url.split('/')[-1]
            print('comment delete', comment_id)
            c: Comment = Comment.query.get(comment_id)
            author_id = c.author_id
            topic_id = c.topic_id
            topic_author_id = Topic.query.get(topic_id).author_id

            if current_user.can(permission) or author_id == current_user.id or topic_author_id == current_user:
                return f(*args, **kwargs)
            else:
                flash('你没有权限删除此评论')
                return redirect(url_for('topic.detail', id=topic_id))
        return decorated_function
    return decorator


def topic_delete(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            topic_id = request.url.split('/')[-1]
            author_id = Topic.query.get(topic_id).author_id

            if current_user.can(permission) or author_id == current_user.id:
                return f(*args, **kwargs)
            else:
                flash('你没有权限删除此话题')
                return redirect(url_for('topic.index'))
        return decorated_function
    return decorator


def same_user_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        topic_id = request.url.split('/')[-1]
        t = Topic.query.get(topic_id)
        if current_user.id == t.author_id:
            return f(*args, **kwargs)
        else:
            flash('你没有权限修改话题')
            return redirect(url_for('topic.index'))
    return decorator
