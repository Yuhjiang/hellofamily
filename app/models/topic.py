from .. import db
from datetime import datetime
from .comment import Comment
from .reply import Reply


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    title = db.Column(db.String(64))
    created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='topic', lazy='dynamic')
    replies = db.relationship('Reply', backref='topic', lazy='dynamic')

    def json(self):
        d = dict()
        for attr, column in self.__mapper__.c.items():
            if hasattr(self, attr):
                v = getattr(self, attr)
                d[attr] = v
        return d