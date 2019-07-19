from . import face, mongodb
from .forms import FaceForm
from flask import render_template, redirect, url_for
from datetime import datetime


@face.route('/', methods=['GET', 'POST'])
def index():
    form = FaceForm()
    images_db = mongodb['images']
    if form.validate_on_submit():
        print(form.group.data, form.member.data, form.start_time.data, form.end_time.data)
        start_time = datetime.strptime(str(form.start_time.data), '%Y-%m-%d').timestamp()
        end_time = datetime.strptime(str(form.end_time.data), '%Y-%m-%d').timestamp()
        if form.member.data == 'all':
            images = images_db.find(
                {'members.group': form.group.data,
                 'timestamp': {'$gte': start_time, '$lte': end_time}})
        else:
            images = images_db.find(
                {'members.group': form.group.data,
                 'members.name_en': form.member.data,
                 'timestamp': {'$gte': start_time, '$lte': end_time}})
        images = list(images)
        return render_template('face/index.html', form=form, images=images)

    images = list(images_db.find().limit(10))
    return render_template('face/index.html', form=form, images=images)