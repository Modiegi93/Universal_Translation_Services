#!/usr/bin/python3
"""
Translation route
"""
import translator
import requests
import uuid
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from googletrans import Translator, LANGUAGES
from os import getenv
from translator import storage
from translator.translation_model import TranslationModel, Base
from translator.text import TextTranslation
from translator.document import DocumentTranslation
from translator.image import ImageTranslation
from translator.website import WebsiteTranslation
from translator.detect_language import DetectLanguage
from translator.language import LanguageSupport
from translator.feedback import FeedBack
from translator.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ

app = Flask(__name__)


@app.route('/about_us', strict_slashes=False)
def about_us():
    return render_template('about_us.html', cache_id=uuid.uuid4())

@app.route('/translations', strict_slashes=False)
def translations():
    return render_template('translations.html', cache_id=uuid.uuid4())

@app.route('/privacy_terms', strict_slashes=False)
def privacy_terms():
    return render_template('my_account.html', cache_id=uuid.uuid4())


@app.teardown_appcontext
def close_session(exception):
    """Remove the db session or save file"""
    storage.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
