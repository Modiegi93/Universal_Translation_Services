#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
import translator
from translator import storage
from translator.language import LanguageSupport
from googletrans import LANGUAGES
from api.v1.views import app_views

translation_settings = {
    'target_languages': [],
    'default_language': ''
}

@app_views.route('/settings', methods=['GET'], strict_slashes=False)
def get_translation_settings():
    """Get the translation settings"""
    translation_settings = storage.get_translation_settings()
    return jsonify(translation_settings)

@app_views.route('/settings', methods=['POST'], strict_slashes=False)
def update_translation_settings():
    """Update the translation settings"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request body'}), 400

    # Check if the provided target languages are valid
    target_languages = data.get('target_languages')
    if target_languages and not are_valid_languages(target_languages):
        return jsonify({'error': 'Invalid target languages provided'}), 400

    # Check if the provided default language is valid
    default_language = data.get('default_language')
    if default_language and not is_valid_language(default_language):
        return jsonify({'error': 'Invalid default language provided'}), 400

    # Update the translation settings in the storage
    success = storage.save(data)
    if success:
        return jsonify({'message': 'Translation settings updated successfully'})
    else:
        return jsonify({'error': 'Failed to update translation settings'}), 500

def are_valid_languages(languages):
    """Check if the provided languages are valid"""
    valid_languages = get_valid_languages()

    for language in languages:
        if language not in valid_languages:
            return False

    return True

def is_valid_language(language):
    """Check if the provided language is valid"""
    valid_languages = get_valid_languages()

    if language in valid_languages:
        return True

    return False

def get_valid_languages():
    """Get the list of valid languages"""
    valid_languages = []

    for code, name in LANGUAGES.items():
        valid_languages.append({'code': code, 'name': name})

    # Store the valid languages in the database and file storage
    store_valid_languages(valid_languages)

    return valid_languages

def store_valid_languages(languages):
    """Store the valid languages in the database and file storage"""
    for language in languages:
        store_language = Language(code=language['code'], name=language['name'])
        storage.new(store_language)

    storage.save()

    # Store the languages in the file storage
    with open('valid_languages.txt', 'w') as f:
        for language in languages:
            f.write(f"{language['code']}: {language['name']}\n")
