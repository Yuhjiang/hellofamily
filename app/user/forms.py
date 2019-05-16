from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
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

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')


class EditProfileAdminForm(FlaskForm):
    name = StringField('昵称')
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class UpdateIcon(FlaskForm):
    icon = FileField('上传头像')
    submit = SubmitField('上传')


class ChangePasswordForm(FlaskForm):
    """
    已知原始密码，重新设置新密码
    """
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired(), EqualTo('password2', message='两次密码不一致')])
    password2 = PasswordField('Confirm your password', validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    """
    原始密码忘记，通过邮箱找回密码
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    """
    原始密码忘记，重新设置新密码
    """
    password = PasswordField('New password', validators=[DataRequired(), EqualTo('password2', message='两次密码不一致')])
    password2 = PasswordField('Confirm your password', validators=[DataRequired()])
    submit = SubmitField('Update Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.dat).first():
            raise ValidationError('Email already registered.')
