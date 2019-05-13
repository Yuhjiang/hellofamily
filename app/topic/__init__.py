from flask import Blueprint
from ..models.permission import Permission
from flask_login import current_user


topic = Blueprint('topic', __name__)

from . import views


@topic.app_context_processor
def inject_permissions():
    return dict(Permission=Permission, current_user=current_user)
