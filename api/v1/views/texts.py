#!/usr/bin/python3
"""Text translations views"""
from api.v1.views import app_views
from flask import Flask jsonify, abort, request
from translator import storage, TextTranslation
from googletrans import Translator, LANGUAGES

app.config['UPLOAD_FOLDER'] = 'uploads'

translator = Translator(service_urls=['translate.google.com'])

# Get available languages
available_languages = {code: name for code, name in LANGUAGES.items()}

@app.route('/translations/<text_translations>', methods=['POST'])
def translate_text():
    # Check if text is included in the request
    if 'text' not in request.form:
        abort(400, 'No text provided')

    text = request.form['text']

    # Get the target language from the request
    target_language = request.form.get('target_language')

    if not target_language:
        abort(400, 'Target language not specified')

    # Check if the target language is valid
    if target_language not in available_languages:
        abort(400, 'Invalid target language')

    # Detect the source language of the text
    detection_result = translator.detect(text)
    source_language = detection_result.lang

    # Translate the text to the target language
    try:
        translation = translate_text_string(text, source_language, target_language)
        store_text_translation(text, source_language, target_language, translation)
        return jsonify({'translation': translation})
    except Exception as e:
        abort(500, str(e))

def translate_text_string(text, source_language, target_language):
    # Translate the text using the Google Translate library
    result = translator.translate(text, src=source_language, dest=target_language)
    translated_text = result.text

    return translated_text

def store_text_translation(text, source_language, target_language, translated_text):
    # Create a new TextTranslation instance
    new_translation = TextTranslation(text=text,
                                      source_language=source_language,
                                      target_language=target_language,
                                      translated_text=translated_text)

    # Add the translation to the database
    storage.new(new_translation)
    storage.save()

    # Store the translation in file storage
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{new_translation.id}.txt')
    with open(file_path, 'w') as f:
        f.write(translated_text)

@app.route('/translations/<int:translation_id>', methods=['GET'])
def get_translation(translation_id):
    # Retrieve the translation from the database
    translation = session.query(TextTranslation).get(translation_id)
    if not translation:
        abort(404, 'Translation not found')

     # Retrieve the translation from file storage
    filename = secure_filename(f'{translation.id}.txt')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file_path, 'r') as f:
        translated_text = f.read()

    translation.translated_text = translated_text
    return jsonify({'translation': translation.to_dict()})

@app.route('/translations/<language_supported>', methods=['GET'])
def get_languages():
    return jsonify({'languages': available_languages})
