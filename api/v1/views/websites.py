#!/usr/bin/python3
"""Website translations views"""
from flask import Flask, jsonify, request, abort
from urllib.parse import urlparse
import requests
from langid import classify
from bs4 import BeautifulSoup
from translator import storage
from api.v1.views import app_views
from translator.translation_model import TranslationModel, Base
from translator.website import WebsiteTranslation

RAPIDAPI_API_KEY = 'f94d683e50mshe579b860a6a88cap1ebc29jsna3f5e765683f'
RAPIDAPI_HOST = 'rapid-translate-multi-traduction.p.rapidapi.com'

@app_views.route('/websites', methods=['POST'], strict_slashes=False)
def create_website():
    """Create a new website translation"""
    if not request.json or 'url' not in request.json or 'target_lang' not in request.json:
        abort(400, 'Invalid request')

    url = request.json['url']
    target_lang = request.json['target_lang']

    # Perform translation using Rapid Translate Multi Traduction API
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_API_KEY,
        'X-RapidAPI-Host': RAPIDAPI_HOST
    }

    payload = {
        'url': url,
        'target_lang': target_lang
    }

    response = requests.post('https://rapid-translate-multi-traduction.p.rapidapi.com/translate',
                             headers=headers, json=payload)

    if response.status_code == 200:
        translated_text = response.json().get('translated_text')
        source_lang = translation_data.get('source_lang')
        # Store the translation in the database
        translation = WebsiteTranslation(url=url, target_lang=target_lang,
                                         source_lang=source_lang,
                                         translated_text=translated_text)
        storage.new(translation)
        storage.save()
        return jsonify({'website_id': translation.id}), 201
    else:
        abort(response.status_code, 'Translation failed')

@app_views.route('/websites', methods=['GET'], strict_slashes=False)
def get_websites():
    """Get all website translations"""
    translations = storage.all(WebsiteTranslation)
    website_list = [translation.to_dict() for translation in translations.values()]
    return jsonify({'translations': website_list})

@app_views.route('/websites/<website_id>', methods=['GET'], strict_slashes=False)
def get_website(website_id):
    """Get specific website translation"""
    translation = storage.get(WebsiteTranslation, website_id)
    if not translation:
        abort(404, 'Website translation not found')
    return jsonify({
        'id': translation.id,
        'input_text': translation.input_text,
        'source_lang': translation.source_lang,
        'target_lang': translation.target_lang,
        'translated_text': translation.translated_text
    })
    
@app_views.route('/websites/<website_id>', methods=['DELETE'], strict_slashes=False)
def delete_website(website_id):
    """Delete stored website translations"""
    translation = storage.get(WebsiteTranslation, website_id)
    if not translation:
        abort(404, 'Website translation not found')

    storage.delete(translation)
    storage.save()

    return jsonify({'message': 'Website translation deleted'}), 200
