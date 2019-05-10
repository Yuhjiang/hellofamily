from flask import render_template, session, redirect, url_for, current_app, flash, request
from . import auth
from flask_login import login_user, login_required, logout_user, current_user
from ..models.user import User
from .. import db
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            return redirect('/')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('auth/login.html', form=form)
