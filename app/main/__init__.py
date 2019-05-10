from flask import Blueprint
from ..models.permission import Permission

main = Blueprint('main', __name__)

from . import views
# @main.app_context_processor
# def inject_permissions():
#     """
#     访问main的路由时，增加权限验证
#     :return:
#     """
#     return dict(Permission=Permission)
