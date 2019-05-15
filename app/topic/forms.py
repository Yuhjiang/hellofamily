from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class TopicForm(FlaskForm):
    title = StringField('输入标题', validators=[DataRequired()])
    body = TextAreaField('输入内容', validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    topic_id = IntegerField()
    topic_user_id = IntegerField()
    body = TextAreaField('输入评论', validators=[DataRequired()])
    submit = SubmitField('评论')
