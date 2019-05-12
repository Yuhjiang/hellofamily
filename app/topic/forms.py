from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class TopicForm(FlaskForm):
    title = StringField('输入标题', validators=[DataRequired()])
    body = TextAreaField('输入内容', validators=[DataRequired()])
    submit = SubmitField('提交')
