from .. import db
from datetime import datetime
from .comment import Comment
from .reply import Reply
from flask import url_for
from app.exceptions import ValidationError


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    title = db.Column(db.String(64))
    created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    replies = db.relationship('Reply', backref='topic', lazy='dynamic')
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))

    def json(self):
        d = dict()
        for attr, column in self.__mapper__.c.items():
            if hasattr(self, attr):
                v = getattr(self, attr)
                d[attr] = v
        return d

    def to_json(self) -> dict:
        """
        适用于REST API的dict格式的topic数据，返回数据后会在路由中jsonify处理
        :return:字典格式的topic数据
        """
        json_topic = {
            'url': url_for('api.get_topic', id=self.id),
            'title': self.title,
            'body': self.body,
            'timestamp': self.created_time,
            # 'author_url': url_for('api.get_user', id=self.author_id),
            # 'comments_url': url_for('api.get_topic_comments', id=self.id),
            'comment_count': self.comments.count(),
        }
        return json_topic

    @staticmethod
    def from_json(json_topic):
        """
        利用API发送的json数据生成新的topic
        :param json_topic: request.json
        :return: 新Topic对象, author信息在api.new_topic()中完善
        """
        body = json_topic.get('body')
        title = json_topic.get('title')
        print(body, title)
        if body is None or body == '' or title is None or title == '':
            raise ValidationError('Topic doest not have a body or title')
        return Topic(body=body, title=title)
