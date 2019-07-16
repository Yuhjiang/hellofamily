from flask import Blueprint
from flask import session
from flask_socketio import emit, join_room, leave_room, SocketIO
from flask_login import current_user

socketio = SocketIO()

chatroom = Blueprint('chatroom', __name__)

from . import views


@socketio.on('join', namespace='/chatroom')
def join(data):
    """
    加入一个room
    :param data: 前端发送包含room的数据
    """
    room = data['room']
    join_room(room)
    session['room'] = room
    name = current_user.name
    message = '用户: ({}) 进入了房间'.format(name)
    d = dict(
        message=message,
    )
    emit('status', d, room=room)


@socketio.on('send', namespace='/chatroom')
def send(data):
    room = session.get('room')
    name = current_user.name
    message = data.get('message')
    formatted = '{}: {}'.format(name, message)
    d = dict(
        message=formatted,
    )
    emit('message', d, room)


@socketio.on('leave', namespace='/chatroom')
def leave(data):
    room = session.get('room')
    leave_room(room)
    name = current_user.name
    d = dict(
        message='{} 离开了房间'.format(name),
    )
    emit('status', d, room=room)
