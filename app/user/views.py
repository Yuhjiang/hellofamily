from flask import render_template, session, redirect, url_for, current_app, flash, request
from . import user
from flask_login import login_user, login_required, logout_user, current_user
from ..models.user import User
from .. import db
from .forms import LoginForm, RegistrationForm, EditProfileAdminForm, UpdateIcon, \
    ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from werkzeug.utils import secure_filename
import os
from ..mail import send_email


# @user.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.ping()
#         # 未激活 and
#         if not current_user.confirmed \
#                 and request.endpoint \
#                 and request.blueprint != 'user' \
#                 and request.endpoint != 'static':
#             return redirect(url_for('user.unconfirmed'))


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
        send_email(user.email, '确认并激活你的账户', 'user/email/confirm', user=user, token=token)
    return render_template('user/login.html', form=form)


@user.route('/logout')
def logout():
    logout_user()
    flash('你已退出当前账号')
    return redirect(url_for('main.index'))


@user.route('/setting')
@login_required
def profile():
    info_form = EditProfileAdminForm()
    icon_form = UpdateIcon()
    info_form.location.data = current_user.location
    info_form.about_me.data = current_user.about_me
    infor_form.name.data = current_user.name

    return render_template('user/setting.html', info_form=info_form, icon_form=icon_form)


@user.route('/information', methods=['POST'])
@login_required
def information():
    form = EditProfileAdminForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        current_user.name = form.name.data
        db.session.add(current_user._get_current_object())
        db.session.commit()

    return redirect('setting')


@user.route('/icon', methods=['POST'])
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

    return redirect('setting')


@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('topic.index'))
    if current_user.confirm(token):
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
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    user = current_user
    send_email(user.email, '确认并激活你的账户', 'user/email/confirm', user=user, token=token)

    return redirect(url_for('topic.index'))


@user.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    已知原始密码，重新设置新密码
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('你的密码已经被重置')
            logout_user()
            return redirect(url_for('topic.index'))
        else:
            flash('无效的密码')

    return render_template('user/change_password.html', form=form)


@user.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    """
    原始密码忘记，通过邮箱找回密码
    """
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_password()
            send_email(user.email, 'Rest Your Password', 'user/email/reset_password',
                       user=user, token=token)
        flash('一封重置密码的邮件已发送，请到邮箱查收')
        return redirect(url_for('user.login'))

    return render_template('user/reset_password.html', form=form)


@user.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    """
    原始密码忘记，重新设置新密码
    """
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('你的密码已经被重置')
            return redirect(url_for('user.login'))
        else:
            return redirect('topic.index')

    return render_template('user/reset_password.html', form=form)


@user.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email,
                       'Confirm your email address',
                       'user/email/change_email',
                       user=current_user, token=token)
            flash('邮箱激活邮件已发送到你的新邮箱')
            return redirect(url_for('topic.index'))
        else:
            flash('无效的邮箱地址或密码错误')
    return render_template('user/change_email.html', form=form)


@user.route('/change_email/<token>')
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('成功修改邮箱地址')
    else:
        flash('激活链接不正确或已过期')
    return redirect(url_for('topic.index'))
