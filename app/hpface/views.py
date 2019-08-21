from . import face, mongodb
from .forms import CpForm, FaceForm
from flask import render_template, request, jsonify
from datetime import datetime
from app.utils import paginate


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
    page = request.args.get('page', 1, type=int)

    images = images_db.find().sort('timestamp', -1)

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
        images = images

    pagination = paginate(images, page, 20)
    images = pagination.items

    return render_template('face/index.html', form=form, cpform=cpform, images=images, pagination=pagination, endpoint='face.index')


@face.route('/normal/', methods=['GET'])
def normal():
    form = FaceForm()
    cpform = CpForm()
    images_db = mongodb['images']

    group = request.args.get('group')
    member = request.args.get('member')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    page = request.args.get('page', 1, type=int)

    start_timestamp = datetime.strptime(str(start_time), '%Y-%m-%d').timestamp()
    end_timestamp = datetime.strptime(str(end_time), '%Y-%m-%d').timestamp()
    if member == 'all':
        images = images_db.find(
            {'members.group': group,
             'timestamp': {'$gte': start_timestamp, '$lte': end_timestamp}}).sort('timestamp', -1)
    else:
        images = images_db.find(
            {'members.name_en': member,
             'timestamp': {'$gte': start_timestamp, '$lte': end_timestamp}}).sort('timestamp', -1)

    pagination = paginate(images, page, 20)
    images = pagination.items

    search = {'group': group, 'member': member, 'start_time': start_time, 'end_time': end_time}
    return render_template('face/normal.html', form=form, cpform=cpform, images=images, pagination=pagination, endpoint='face.normal', search=search)


@face.route('/cp/', methods=['GET'])
def cp():
    form = FaceForm()
    cpform = CpForm()
    images_db = mongodb['images']

    member1 = request.args.get('member1')
    member2 = request.args.get('member2')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    page = request.args.get('page', 1, type=int)

    mem1, mem2 = search_members(member1), search_members(member2)
    start_timestamp = datetime.strptime(str(start_time), '%Y-%m-%d').timestamp()
    end_timestamp = datetime.strptime(str(end_time), '%Y-%m-%d').timestamp()
    # 寻找CP，限定两人
    images = images_db.find({'members': {'$all': [mem1, mem2]},
                             'timestamp': {'$gte': start_timestamp, '$lte': end_timestamp}, 'size': 2}).sort('timestamp', -1)

    pagination = paginate(images, page, 20)

    images = pagination.items

    search = {'member1': member1, 'member2': member2, 'start_time': start_time, 'end_time': end_time}
    return render_template('face/cp.html', form=form, cpform=cpform, images=images, pagination=pagination, endpoint='face.cp', search=search)