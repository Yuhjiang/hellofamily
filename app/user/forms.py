from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models.user import User
from wtforms import ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_/]*$', 0,
                                                          'Username must have only letters, '
                                                          'numbers, dots or underscores')
                                                   ])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired(), Length(1, 64)])


class EditProfileAdminForm(FlaskForm):
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class UpdateIcon(FlaskForm):
    icon = FileField('上传头像')
    submit = SubmitField('上传')
