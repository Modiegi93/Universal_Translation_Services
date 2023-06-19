#!/usr/bin/python3
"""Text translations views"""
import os
import requests
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from translator import storage
from langdetect import detect
from translator.translation_model import TranslationModel, Base
from translator.text import TextTranslation

RAPIDAPI_API_KEY = 'f94d683e50mshe579b860a6a88cap1ebc29jsna3f5e765683f'
RAPIDAPI_HOST = 'google-translate1.p.rapidapi.com'


@app_views.route('/texts', methods=['GET'], strict_slashes=False)
def get_texts():
    """Get all text translations"""
    translations = storage.all(TextTranslation)
    translation_list = [translation.to_dict() for translation in translations.values()]
    return jsonify({'translations': translation_list})

@app_views.route('/texts/<text_id>', methods=['GET'],
                 strict_slashes=False)
def get_text(text_id):
    """Get specific text translations"""
    translation = storage.get(TextTranslation, text_id)
    if not translation:
        abort(404, 'Text translation not found')
    return jsonify({
        'id': translation.id,
        'input_text': translation.input_text,
        'source_lang': translation.source_lang,
        'target_lang': translation.target_lang,
        'translated_text': translation.translated_text
    })

@app_views.route('/texts', methods=['POST'], strict_slashes=False)
def create_text():
    """Create text translations"""
    if not request.json or 'text' not in request.json or 'target_lang' not in request.json:
        abort(400, 'Invalid request')

    input_text = request.json['text']
    target_lang = request.json['target_lang']

    headers = {
        'X-RapidAPI-Key': RAPIDAPI_API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-RapidAPI-Host': RAPIDAPI_HOST
    }

    payload = {
        'q': input_text,
        'target': target_lang
    }

    try:
        response = requests.post('https://google-translate1.p.rapidapi.com/language/translate/v2', headers=headers, data=payload)
        translation = response.json()['data']['translations'][0]['translatedText']
        
        # Detect source language
        source_lang = detect(input_text)

        # Store the translation in the database
        new_translation = TextTranslation(input_text=input_text,
                                          target_lang=target_lang,
                                          source_lang=source_lang,
                                          translated_text=translation)
        storage.new(new_translation)
        storage.save()

        return jsonify({'translated_text': translation}), 200
    except Exception as e:
        abort(500, str(e))

@app_views.route('/texts/<text_id>', methods=['DELETE'], strict_slashes=False)
def delete_text_translation(text_id):
    """Delete stored text translations"""
    translation = storage.get(TextTranslation, text_id)
    if not translation:
        abort(404, 'Text translation not found')

    storage.delete(translation)
    storage.save()

    return jsonify({'message': 'Text translation deleted'}), 200
