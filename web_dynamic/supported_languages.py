#!/usr/bin/python3
"""
Starts a Flask Web application
"""
import uuid
from flask import Flask, jsonify, request, render_template
from translator import storage
from translator.translation_model import TranslationModel, Base
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from googletrans import LANGUAGES
app = Flask(__name__)


@app.route('/supported_languages', strict_slashes)
def get_supported_languages():
    supported_languages = {code: name for code, name in
                           sorted(LANGUAGES.items(), key=lambda x: x[1])}
    return jsonify(supported_languages)

@app.route('/languages', strict_slashes)
def render_language_selector():
    supported_languages = {code: name for code, name in sorted(LANGUAGES.items(), key=lambda x: x[1])}
    return render_template('languages.html', supported_languages=supported_languages,
                            cache_id=uuid.uuid4())


@app.teardown_appcontext
def close_session(exception):
    """Remove the db session or save file"""
    storage.close()

if __name__ = "__main__":
    app.run(host="0.0.0.0", port="5000")
