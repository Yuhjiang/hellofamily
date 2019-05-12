from .forms import TopicForm
from ..models.user import User
from ..models.topic import Topic
from flask_login import login_required, login_user, current_user
from .. import db
from . import topic
from flask import render_template, redirect


@topic.route('/')
@login_required
def index():
    topics = Topic.query.order_by(Topic.created_time.desc()).all()

    return render_template('topic/index.html', topics=topics)


@topic.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TopicForm()
    if form.validate_on_submit():
        t = Topic(title=form.title.data,
                  body=form.body.data,
                  author_id=current_user.id,
                      )
        db.session.add(t)
        db.session.commit()
        return redirect('/')
    return render_template('topic/add.html', form=form)


@topic.route('/detail/<int:id>', methods=['GET'])
def detail(id):
    return redirect('/')