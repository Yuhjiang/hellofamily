from flask import Blueprint


user = Blueprint('people', __name__)


from . import views