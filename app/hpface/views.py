from . import face, mongodb
from .forms import CpForm, FaceForm
from flask import render_template, redirect, url_for, request, jsonify
from datetime import datetime


def search_members(member):
    """
    获取成员的信息用于cp查询
    :param member: name_en
    :return: dict
    """
    members_db = mongodb['members']
    m = members_db.find_one({'name_en': member})

    return {'_id': m['_id'], 'name_en': m['name_en'], 'name_jp': m['name_jp'], 'group': m['group']}


@face.route('/', methods=['GET', 'POST'])
def index():
    form = FaceForm()
    cpform = CpForm()
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
                {'members.name_en': form.member.data,
                 'timestamp': {'$gte': start_time, '$lte': end_time}})
        images = list(images)
        return render_template('face/index.html', form=form, cpform=cpform, images=images)

    # if cpform.validate_on_submit():
    #     print(cpform.member1.data, cpform.member2.data, cpform.start_time.data, cpform.end_time.data)
    #     start_time = datetime.strptime(str(cpform.start_time.data), '%Y-%m-%d').timestamp()
    #     end_time = datetime.strptime(str(cpform.end_time.data), '%Y-%m-%d').timestamp()
    #     member1, member2 = search_members(cpform.member1.data), search_members(cpform.member2.data)
    #     images = images_db.find({'members': {'$all': [member1, member2]},
    #                              'timestamp': {'$gte': start_time, '$lte': end_time}})
    #     images = list(images)
    #     return render_template('face/index.html', form=form, cpform=cpform, images=images)

    images = list(images_db.find().limit(10))
    return render_template('face/index.html', form=form, cpform=cpform, images=images)


@face.route('/cp', methods=['POST'])
def cp():
    data = request.json
    images_db = mongodb['images']
    start_time = datetime.strptime(data['start_time'], '%Y-%m-%d').timestamp()
    end_time = datetime.strptime(data['end_time'], '%Y-%m-%d').timestamp()
    member1, member2 = search_members(data['member1']), search_members(data['member2'])
    images = images_db.find({'members': {'$all': [member1, member2]},
                             'timestamp': {'$gte': start_time, '$lte': end_time}})
    images = filter(lambda img: len(img['members']) == 2, list(images))

    res = []
    for img in images:
        res.append({
            'url': img['url'],
            'timestamp': img['timestamp'],
            'members': [m['name_en'] for m in img['members']]
        })
    return jsonify(res)
