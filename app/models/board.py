from .. import db
from .user import User


class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(40), index=True)
    body = db.Column(db.Text)
    topics = db.relationship('Topic', backref='board', lazy='dynamic')

    @staticmethod
    def insert_board():
        boards = ['一般话题', 'HELLO! PROJECT', 'モーニング娘。',
                  'アンジュルム', 'Juice=Juice', 'カントリー・ガールズ',
                  'こぶしファクトリー', 'つばきファクトリ', 'BEYOOOOONDS']
        for b in boards:
            board = Board.query.filter_by(name=b).first()
            if board is None:
                board = Board(name=b)
            db.session.add(board)
            db.session.commit()

    def __repr__(self):
        return '<Board {}>'.format(self.name)
