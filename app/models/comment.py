from .. import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    reply = db.relationship('Reply', backref='comment', lazy='dynamic', cascade='all, delete-orphan')

    def json(self):
        d = dict()
        for attr, column in self.__mapper__.c.items():
            if hasattr(self, attr):
                v = getattr(self, attr)
                d[attr] = v
        return d
