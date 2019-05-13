from flask import render_template, session, redirect, url_for, current_app, flash, request
from . import user
from flask_login import login_user, login_required, logout_user, current_user
from ..models.user import User
from .. import db
from .forms import LoginForm, RegistrationForm, EditProfileAdminForm, UpdateIcon
from werkzeug.utils import secure_filename
import os
from ..email import send_email


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            next:str = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('topic.index')
            flash('登录成功，欢迎{}大人'.format(user.username))
            return redirect(next)
    return render_template('user/login.html', form=form)


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认并激活你的账户', 'user/confirm', user=user, token=token)
    return render_template('user/login.html', form=form)


@user.route('/logout')
def logout():
    logout_user()
    flash('你已退出当前账号')
    return redirect(url_for('main.index'))


@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileAdminForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me

    return render_template('user/profile.html', form=form)


@user.route('/icon', methods=['GET', 'POST'])
@login_required
def icon():
    form = UpdateIcon()
    if form.validate_on_submit():
        filename = secure_filename(form.icon.data.filename)
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'static/images/' + filename)
        current_user.icon = '/static/images/' + filename
        form.icon.data.save(filepath)
        db.session.add(current_user._get_current_object())
        db.session.commit()

    return render_template('user/icon.html', form=form)


@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('topic.index'))
    if current_user.confirmed(token):
        db.session.commit()
        flash('成功激活账户')
    else:
        flash('激活链接不正确或已过期')
    return redirect(url_for('topic.index'))


@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('topic.index'))
    return render_template('user/unconfirmed.html')


@user.route('/resend_confirmation')
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    user = current_user
    send_email(user.email, '确认并激活你的账户', 'user/confirm', user=user, token=token)

    return redirect(url_for('topic.index'))
