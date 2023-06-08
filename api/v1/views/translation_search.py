#!/usr/bin/python3
"""Translation Search"""

from flask import Flask, request, jsonify, abort
from googletrans import Translator
from translator import storage, TranslationModel

@app_views.route('/translation_search', methods=['POST'])
def translation_search():
    if not request.is_json:
        abort(400, 'Not a JSON')

    json_data = request.get_json()
    keyword = json_data.get('keyword')

    if not keyword:
        abort(400, 'Missing required fields')

    translations = storage.all(TranslationModel).values()
    search_results = [translation for translation in translations
                      if translation.search(keyword)]

    return jsonify([translation.to_dict() for translation in search_results])
