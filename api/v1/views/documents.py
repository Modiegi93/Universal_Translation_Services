#!/usr/bin/python3
"""Document translations views"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, send_from_directory
from translator import storage, DocumentTranslation
from googletrans Translator, LANGUAGES
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'}

translator = Translator(service_urls=['translate.google.com'])

# Helper function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Get available languages
available_languages = {code: name for code, name in LANGUAGES.items()}

@app.route('/translations/<document_translations>', methods=['POST'])
def translate_document():
    # Check if a file is included in the request
    if 'file' not in request.files:
        abort(400, 'No file provided')

    file = request.files['file']

    # Check if the file has an allowed extension
    if not allowed_file(file.filename):
        abort(400, 'Invalid file extension')

    # Get the target language from the request
    target_language = request.form.get('target_language')

    if not target_language:
        abort(400, 'Target language not specified')

    # Check if the target language is valid
    if target_language not in available_languages:
        abort(400, 'Invalid target language')

    # Translate the document
    try:
        translation = translate_document_file(file, target_language)
        return jsonify({'translation': translation.to_dict()})
    except Exception as e:
        abort(500, str(e))

def translate_document_file(file, target_language):
    # Save the file to the uploads folder
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Detect the source language of the document
    with open(file_path, 'r', encoding='utf-8') as f:
        source_text = f.read()

    # Detect the source language using Google Translate library
    detection_result = translator.detect(source_text)
    source_language = detection_result.lang

    # Translate the document using the Google Translate library
    result = translator.translate(source_text, src=source_language,
                                  dest=target_language)
    translated_text = result.text

    # Store the translation in the database
    translation = DocumentTranslation(filename=filename,
                                     source_language=source_language,
                                     target_language=target_language,
                                     translated_text=translated_text)
    storage.new(translation)
    storage.save()

    # Delete the uploaded file
    os.remove(file_path)

    return translation

@app.route('/download/<int:translation_id>', methods=['GET'])
def download_translation(translation_id):
    translation = session.query(DocumentTranslation).get(translation_id)
    if not translation:
        abort(404, 'Translation not found')

    # Generate a downloadable text file with the translated text
    translated_filename = f'translation_{translation.id}.txt'
    translated_filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                       translated_filename)
    with open(translated_filepath, 'w', encoding='utf-8') as f:
        f.write(translation.translated_text)

    return send_from_directory(app.config['UPLOAD_FOLDER'], translated_filename,
                               as_attachment=True)

@app.route('/translations/<language_supported>', methods=['GET'])
def get_languages():
    return jsonify({'languages': available_languages})
