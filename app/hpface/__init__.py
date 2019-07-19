from flask import Blueprint
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
mongodb = client['helloproject']

face = Blueprint('face', __name__)

from . import views