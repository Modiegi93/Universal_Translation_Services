#!/usr/bin/python3
""" import views"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.texts import *
from api.v1.views.documents import *
from api.v1.views.images import *
from api.v1.views.websites import *
from api.v1.views.feedback_translation import *
from api.v1.views.translation_search import *
from api.v1.views.translation_history import *
from api.v1.views.users import *
from api.v1.views.index import *
from api.v1.views.translation_settings import *
