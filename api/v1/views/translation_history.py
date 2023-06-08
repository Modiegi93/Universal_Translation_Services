#!/usr/bin/python3
"""Translations history"""
from flask import Flask, request, jsonify, abort
from translator import storage, TranslationModel


@app_views.route('/translation_history', methods=['GET', 'POST'])
def translation_history():
    if request.method == 'GET':
        translations = storage.all(TranslationModel).values()
        return jsonify([translation.to_dict() for translation in translations])

    elif request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')

        json_data = request.get_json()
        source_text = json_data.get('source_text')
        target_language = json_data.get('target_language')
        translated_text = json_data.get('translated_text')

        if not source_text or not target_language or not translated_text:
            abort(400, 'Missing required fields')

        new_translation = TranslationModel(input_text=source_text,
                                             target_language=target_language,
                                             translated_text=translated_text)
        storage.new(new_translation)
        storage.save()

        return jsonify(new_translation.to_dict())

@app_views.route('/translation_history/<translation_id>', methods=['PUT', 'DELETE'])
def history_details(translation_id):
    translation = storage.get(TranslationModel, translation_id)
    if not translation:
        abort(404)

    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')

        json_data = request.get_json()
        source_text = json_data.get('source_text')
        target_language = json_data.get('target_language')
        translated_text = json_data.get('translated_text')

        if not source_text or not target_language or not translated_text:
            abort(400, 'Missing required fields')

        translation.source_text = source_text
        translation.target_language = target_language
        translation.translated_text = translated_text
        storage.save()

        return jsonify(translation.to_dict())

    elif request.method == 'DELETE':
        storage.delete(translation)
        storage.save()
        return jsonify({'message': 'Translation deleted'})
