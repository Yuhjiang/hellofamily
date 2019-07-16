from . import chatroom
from flask import render_template


@chatroom.route('/')
def index():
    return render_template('chatroom/index.html')