#!/usr/bin/python3
"""Website translations views"""
from flask import Flask, jsonify, request, abort
from googletrans import Translator, LANGUAGES
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

translator = Translator(service_urls=['translate.google.com'])

available_languages = {code: name for code, name in LANGUAGES.items()}

@app.route('/translations/<website_translations> ', methods=['POST'])
def translate_website():
    # Get the website URL and target language from the request
    website_url = request.form.get('website_url')
    target_language = request.form.get('target_language')

    if not website_url:
    abort(400, 'Website URL not specified')

    if not target_language:
        abort(400, 'Target language not specified')

    # Check if the target language is valid
    if target_language not in available_languages:
        abort(400, 'Invalid target language')

    # Translate the website
    try:
        translation = translate_website_content(website_url, target_language)
        return jsonify({'translation': translation.to_dict()})
    except Exception as e:
        abort(500, str(e))

def translate_website_content(website_url, target_language):
    # Fetch the HTML content from the website
    response = requests.get(website_url)
    if response.status_code != 200:
        abort(500, 'Failed to fetch website content')
    html_content = response.text

    # Detect the source language of the HTML content
    detection_result = translator.detect(html_content)
    source_language = detection_result.lang

    # Translate the HTML content to the target language
    translated_content = translate_text_string(html_content, source_language,
                                               target_language)

    # Create a new WebsiteTranslation instance
    new_translation = WebsiteTranslation(url=website_url,
                                         source_language=source_language,
                                         target_language=target_language,
                                         translated_content=translated_content)

    # Add the translation to the database
    storage.new(new_translation)
    storage.save()

    return new_translation

def translate_text_string(text, source_language, target_language):
    # Translate the text using the Google Translate library
    result = translator.translate(text, src=source_language, dest=target_language)
    translated_text = result.text
    return translated_text

@app.route('/translations/int:translation_id', methods=['GET'])
def get_translation(translation_id):
    # Retrieve the translation from the database
    translation = session.query(WebsiteTranslation).get(translation_id)
    if not translation:
        abort(404, 'Translation not found')
    return jsonify({'translation': translation.to_dict()})

@app.route('/translations/<language_supported>', methods=['GET'])
def get_languages():
    return jsonify({'languages': available_languages})
