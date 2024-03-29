from flask import Blueprint
from ..models.permission import Permission
from flask_login import current_user
import redis
import json
from ..models.topic import Topic
from ..models.comment import Comment
from ..models.user import User
from ..models.reply import Reply
from ..models.board import Board

cache = redis.StrictRedis()


def created_topic(author_id):
    """
    创建主题
    :param author_id: 当前用户id
    :return:
    """
    # 创建用户对应的键值
    k = 'created_topic_{}'.format(author_id)
    if cache.exists(k):
        v = cache.get(k)
        topics = json.loads(v)
        return topics
    else:
        return update_topics(author_id)


def update_topics(author_id):
    k = 'created_topic_{}'.format(author_id)
    topics = Topic.query.filter_by(author_id=author_id).order_by(Topic.created_time.desc())
    v = []
    for t in topics:
        t = t.json()
        t['created_time'] = t['created_time'].strftime('%Y-%m-%d %H:%M:%S')
        v.append(t)
    v = json.dumps(v)
    cache.set(k, v)
    cache.expire(k, 3600)
    return topics


def commented_topic(author_id):
    """
    评论过的主题
    :param author_id: 当前用户id
    :return:
    """
    # 创建用户对应的键值
    k = 'commented_topic_{}'.format(author_id)
    if cache.exists(k):
        v = cache.get(k)
        topics = json.loads(v)
        return topics
    else:
        return update_commented_topics(author_id)


def update_commented_topics(author_id):
    k = 'commented_topic_{}'.format(author_id)
    comments = Comment.query.filter_by(author_id=author_id).order_by(Comment.created_time.desc()).limit(10).all()
    topics = []
    # 获取评论过的所有主题
    for c in comments:
        t = Topic.query.get(c.topic_id).json()
        t['created_time'] = t['created_time'].strftime('%Y-%m-%d %H:%M:%S')
        topics.append(t)
    v = json.dumps([t for t in topics])
    cache.set(k, v)
    cache.expire(k, 3600)
    return topics


def users_from_comment(comment):
    parts = comment.split()
    users = []

    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.query.filter_by(username=username).first()
            if u is not None:
                users.append(u)
    return users


def replied_comment(receiver_id):
    k = 'replied_comment_{}'.format(receiver_id)
    if cache.exists(k):
        v = cache.get(k)
        comments = json.loads(v)
        return comments
    else:
        return update_replied_comment(receiver_id)


def update_replied_comment(receiver_id):
    k = 'replied_comment_{}'.format(receiver_id)
    v = []
    comments = Reply.query.filter_by(receiver_id=receiver_id).all()
    for c in comments:
        c = c.json()
        c['created_time'] = c['created_time'].strftime('%Y-%m-%d %H:%M:%S')
        v.append(c)
    v = json.dumps(v)
    cache.set(k, v)
    cache.expire(k, 3600)
    return comments


topic = Blueprint('topic', __name__)

from . import views


@topic.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@topic.app_context_processor
def inject_boards():
    return dict(boards=Board.query.all())