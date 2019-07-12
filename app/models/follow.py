"""
处理用户关注与被关注的多对多关系
"""
from .. import db
from datetime import datetime


class Follow(db.Model):
    __tablename__ = 'follows'
    # 联合主键
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
