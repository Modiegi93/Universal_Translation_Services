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

app = Flask(__name__)

translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translations/<language_supported>')
def get_languages():
    available_languages = {code: name for code, name in LANGUAGES.items()}
    return render_template('languages.html', languages=available_languages)

@app.route('/translation_history')
def render_translation_history():
    """Render the translation history template with all translations"""
    translations = storage.all("TextTranslation", "DocumentTranslation",
                               "ImageTranslation", "WebsiteTranslation").values()
    return render_template("translation_history.html",
                           Query_name="Translation History", translations=translations)


@app.teardown_appcontext
def close_session(exception):
    """Remove the db session or save file"""
    storage.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
