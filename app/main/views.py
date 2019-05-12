from flask import render_template, session, redirect, url_for, current_app, flash
from . import main
from .. import db
from ..models.user import User
from ..models.role import Role


@main.route('/')
def index():
    return render_template('index.html')
