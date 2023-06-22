#!/usr/bin/python3
"""Getting languages"""
import requests
import os
import requests
from langdetect import detect
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from translator import storage
from translator.language import LanguageSupport
from translator.detect_language import DetectLanguage
from translator.translation_model import TranslationModel, Base
from googletrans import LANGUAGES

@app_views.route('/supported_languages', methods=['GET'], strict_slashes=False)
def get_supported_languages():
    supported_languages = {code: name for code, name in
                           sorted(LANGUAGES.items(), key=lambda x: x[1])}
    return jsonify(supported_languages)

@app_views.route('/detect', methods=['POST'], strict_slashes=False)
def detect_language():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid request. Missing "text" parameter.'}), 400

    text = data['text']

    try:
        detected_language = detect(text)
        return jsonify({'language': detected_language}), 200

    except Exception as e:
        return jsonify({'error': 'Language detection failed. Reason: ' +
                       str(e)}), 500
