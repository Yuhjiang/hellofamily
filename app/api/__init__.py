from flask import Blueprint

api = Blueprint('api', __name__)

# from . import authentication, topics, users, comments, errors
from . import authentication, topics, errors
