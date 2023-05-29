#!/usr/bin/python3
""" import views"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

#from api.v1.views.texts import *
#from api.v1.views.documents import *
#from api.v1.views.image import *
#from api.v1.views.websites import *
#from api.v1.views.feedbacks import *
#from api.v1.views.language_support import *
#from api.v1.views.detect_languages import *
#from api.v1.views.users import *
from api.v1.views.index import *
