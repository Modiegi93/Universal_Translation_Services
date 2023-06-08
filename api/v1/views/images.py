#!/usr/bin/python3
"""Image translations views"""
from flask import Flask, jsonify, request, abort, send_from_directory
from werkzeug.utils import secure_filename
from googletrans import Translator, LANGUAGES
from PIL import Image
import pytesseract
from translator import storage, ImageTranslation

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

translator = Translator(service_urls=['translate.google.com'])

# Helper function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Get available languages
available_languages = {code: name for code, name in LANGUAGES.items()}

@app.route('/translations/<image_translations>', methods=['POST'])
def translate_image():
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

    # Translate the image
    try:
        translated_text, detected_language, language_support,
        language_code = translate_image_file(file, target_language)
        return jsonify({'translation': translation.to_dict()})
    except Exception as e:
        abort(500, str(e))

def translate_image_file(file, target_language):
    # Save the file to the uploads folder
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Read the image using Pillow
    image = Image.open(file_path)

    # Extract text from the image using pytesseract
    extracted_text = pytesseract.image_to_string(image)

    # Detect the language of the extracted text
    detected = translator.detect(extracted_text)
    detected_language = detected.lang

    # Translate the extracted text to the target language using the Google Translate library
    result = translator.translate(extracted_text, src=detected_language,
                                  dest=target_language)
    translated_text = result.text

    # Store the translation in the database
    translation = ImageTranslation(filename=filename,
                                  source_language=detected_language,
                                  target_language=target_language,
                                  translated_text=translated_text)
    storage.new(translation)
    storage.save()

    storage_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                f"{new_translation.id}.txt")
    with open(storage_path, 'w') as f:
        f.write(translated_text)

    # Delete the uploaded file
    os.remove(file_path)

    return new_translation

@app.route('/translations/int:translation_id', methods=['GET'])
def get_translation(translation_id):
    # Retrieve the translation from the database
    translation = session.query(ImageTranslation).get(translation_id)
    if not translation:
        abort(404, 'Translation not found')

    # Retrieve the translated text from file storage
    storage_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{translation.id}.txt")
    with open(storage_path, 'r') as f:
        translated_text = f.read()

    translation.translated_text = translated_text
    return jsonify({'translation': translation.to_dict()})

@app.route('/translations/<language_supported>', methods=['GET'])
def get_languages():
    return jsonify({'languages': available_languages})
