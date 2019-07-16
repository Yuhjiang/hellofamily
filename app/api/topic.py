from flask import jsonify, request, url_for, g
from . import api
from ..models.topic import Topic
from ..models.permission import Permission
from .. import db
from .decorators import permission_required
from .errors import forbidden


@api.route('/topics/', methods=['POST'])
@permission_required(Permission.WRITE)      # 验证是否有WRITE权限
def new_topic():
    """
    API创建一个新的topic
    :return: 返回json格式的刚创建的topic, http状态码，新topic的资源位置
    """
    topic = Topic.from_json(request.json)   # 仅包含body
    topic.author = g.current_user           # 添加author
    db.session.add(Topic)
    db.session.commit()

    return jsonify(topic.to_json()), 201, {'Location': url_for('api.get_topic', id=topic.id)}


@api.route('/topics/')
def get_topics():
    """
    获取所有topics
    :return: {topics: [topic1, topic2, topic3...]}
    """
    topics = Topic.query.all()

    return jsonify({'topics': [topic.to_json()] for topic in topics})


@api.route('/topics/<int:id>')
def get_topic(id):
    """
    返回指定id的topic
    :param id: topic的id
    :return: json格式化的topic
    """
    topic = Topic.query.get_or_404(id)

    return jsonify(topic.to_json())


@api.route('/topics/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_topic(id):
    """
    更新topic资源，需验证用户写权限以及被更新的topic和更新者是否为同一个用户
    :param id: topic的id
    :return: 返回json格式化的topic
    """
    topic = Topic.query.get_or_404(id)
    if g.current_user != topic.author_id and not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permission')
    topic.body = request.json.get('body', topic.body)
    db.session.add(topic)
    db.session.commit()

    return jsonify(topic.to_json())