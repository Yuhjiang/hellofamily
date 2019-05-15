from .forms import TopicForm, CommentForm
from ..models.user import User
from ..models.topic import Topic
from flask_login import login_required, login_user, current_user
from .. import db
from . import topic, created_topic, commented_topic, replied_comment, users_from_comment
from ..models.comment import Comment
from ..models.reply import Reply
from flask import render_template, redirect, url_for


@topic.route('/')
def index():
    topics = Topic.query.order_by(Topic.created_time.desc()).all()

    return render_template('topic/index.html', topics=topics)


@topic.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TopicForm()
    if form.validate_on_submit():
        t = Topic(title=form.title.data,
                  body='\n'+form.body.data,
                  author_id=current_user.id
                  )
        db.session.add(t)
        db.session.commit()
        return redirect('/topic')
    return render_template('topic/add.html', form=form)


@topic.route('/detail/<int:id>')
def detail(id):
    form = CommentForm()
    t = Topic.query.get(id)
    comments = Comment.query.filter_by(topic_id=t.id).all()

    return render_template('topic/detail.html', topic=t, comments=comments,  form=form)


@topic.route('/comment/add', methods=['POST'])
@login_required
def comment_add():
    form = CommentForm()
    if form.validate_on_submit():
        users = users_from_comment(form.body.data)
        for user in users:
            reply = Reply(body=form.body.data, author_id=current_user.id, receiver_id=user.id, topic_id=form.topic_id.data)
            db.session.add(reply)
        comment = Comment(
            body=form.body.data,
            topic_id=form.topic_id.data,
            author_id=current_user.id,
        )
        db.session.add(comment)
        db.session.commit()

    return redirect(url_for('topic.detail', id=form.topic_id.data))


@topic.route('/profile')
@login_required
def profile():
    # topics = Topic.query.filter_by(author_id=current_user.id).order_by(Topic.created_time.desc()).all()
    topics = created_topic(author_id=current_user.id)
    # commented_topics = Comment.query.filter_by(author_id=current_user.id).order_by(Comment.created_time.desc()).all()
    commented_topics = commented_topic(author_id=current_user.id)
    # replied_comments = Reply.query.filter_by(receiver_id=current_user.id)
    replied_comments = replied_comment(receiver_id=current_user.id)
    return render_template('topic/profile.html',
                           topics=topics,
                           commented_topics=commented_topics,
                           replied_comments=replied_comments)
