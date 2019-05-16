from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from ..models.board import Board
from ..models.topic import Topic


class TopicForm(FlaskForm):
    title = StringField('输入标题', validators=[DataRequired()])
    board = SelectField('选择板块', coerce=int)
    body = TextAreaField('输入内容', validators=[DataRequired()])
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board.choices = [(board.id, board.name) for board in Board.query.all()]


class CommentForm(FlaskForm):
    topic_id = IntegerField()
    body = TextAreaField('输入评论', validators=[DataRequired()])
    submit = SubmitField('评论')
