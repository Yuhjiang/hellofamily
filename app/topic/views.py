from .forms import TopicForm, CommentForm
from ..models.user import User
from ..models.topic import Topic
from flask_login import login_required, login_user, current_user
from .. import db
from . import topic, created_topic, commented_topic, replied_comment, users_from_comment
from ..models.comment import Comment
from ..models.reply import Reply
from ..models.permission import Permission
from flask import render_template, redirect, url_for, request, flash
from ..decorators import permission_required, admin_required, comment_delete, topic_delete, same_user_required


@topic.route('/')
def index():
    topics = Topic.query.order_by(Topic.created_time.desc()).all()

    return render_template('topic/index.html', topics=topics)


@topic.route('/<int:board_id>')
def board_index(board_id):
    topics = Topic.query.filter_by(board_id=board_id).order_by(Topic.created_time.desc()).all()

    return render_template('topic/index.html', topics=topics)


@topic.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TopicForm()
    if form.validate_on_submit():
        t = Topic(title=form.title.data,
                  body='\n'+form.body.data,
                  author_id=current_user.id,
                  board_id=form.board.data
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
        comment = Comment(
            body=form.body.data,
            topic_id=form.topic_id.data,
            author_id=current_user.id,
        )
        db.session.add(comment)

        users = users_from_comment(form.body.data)
        for user in users:
            reply = Reply(body=form.body.data, author_id=current_user.id, receiver_id=user.id, topic_id=form.topic_id.data, comment_id=comment.id)
            db.session.add(reply)
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


@topic.route('/delete/<int:id>')
@login_required
@topic_delete(Permission.MODERATE)
def delete(id):
    """
    删除topic
    :param id:
    :return:
    """
    t = Topic.query.get(id)
    comments = Comment.query.filter_by(topic_id=id).all()
    for c in comments:
        db.session.delete(c)
    db.session.delete(t)
    db.session.commit()

    return redirect(url_for('.index'))


@topic.route('edit/<int:id>', methods=['GET', 'POST'])
@login_required
@same_user_required
def edit(id):
    """
    修改topic
    :param id:
    :return:
    """
    t = Topic.query.get(id)
    form = TopicForm()
    if form.validate_on_submit():
        t: Topic = Topic.query.get(id)
        t.title = form.title.data
        t.body = '\n' + form.body.data
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('.detail', id=id))
    form.title.data = t.title
    return render_template('topic/edit.html', form=form, topic=t)


@topic.route('comment/delete/<int:id>')
@login_required
@comment_delete(Permission.MODERATE)
def comment_delete(id):
    """
    删除评论
    :param id:
    :return:
    """
    c = Comment.query.get(id)
    replies = Reply.query.filter_by(comment_id=id).all()
    for r in replies:
        db.session.delete(r)
    db.session.delete(c)
    db.session.commit()

    return redirect(url_for('topic.detail', id=c.topic_id))
