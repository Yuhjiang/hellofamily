from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
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
        for i, group in enumerate(list(groups.find())):
            choices.append((group['name_en'], group['name_jp']))
        self.group.choices = choices

        members = mongodb['members']
        choices = [('all', '所有')]
        for i, member in enumerate(list(members.find().sort('group'))):
            choices.append((member['name_en'], member['name_jp']))
        self.member.choices = choices
