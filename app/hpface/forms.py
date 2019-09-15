from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField, StringField
from wtforms.validators import DataRequired
from . import mongodb
from datetime import datetime


class FaceForm(FlaskForm):
    group = SelectField('组合', coerce=str)
    member = SelectField('成员', coerce=str)
    start_time = DateField('开始时间', format='%Y-%m-%d',
                           default=datetime.now())
    end_time = DateField('结束时间', format='%Y-%m-%d',
                         default=datetime.now())
    submit = SubmitField('确认')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        groups = mongodb['groups']

        choices = []
        for group in list(groups.find().sort('sort')):
            choices.append((group['name_en'], group['name_jp']))
        self.group.choices = choices

        members = mongodb['members']
        choices = [('all', '所有')]
        for member in list(members.find().sort('group')):
            choices.append((member['name_en'], member['name_jp']))
        self.member.choices = choices


class CpForm(FlaskForm):
    """
    用于嗑CP的表单
    """
    member1 = SelectField('成员A', coerce=str)
    member2 = SelectField('成员B', coerce=str)
    start_time = DateField('开始时间', format='%Y-%m-%d',
                           default=datetime.now())
    end_time = DateField('结束时间', format='%Y-%m-%d',
                         default=datetime.now())
    submit = SubmitField('确认')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        members = mongodb['members']
        for member in list(members.find().sort('group')):
            choices.append((member['name_en'], member['name_jp']))
        self.member1.choices = choices
        self.member2.choices = choices


class UpdateCookie(FlaskForm):
    """
    更新Cookie值
    """
    cookie = StringField('Cookie', validators=[DataRequired()])
    submit = SubmitField('更新')
