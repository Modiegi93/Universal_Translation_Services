#!/usr/bin/python3
"""Image translations views"""
import requests
from flask import Flask, jsonify, request, abort, send_file
from api.v1.views import app_views
from PIL import Image
import pytesseract
from translate import Translator
from googletrans import Translator, LANGUAGES
from translator import storage
from translator.translation_model import TranslationModel, Base
from translator.image import ImageTranslation
from api.v1.views import app_views
from langdetect import detect

RAPIDAPI_API_KEY = 'f94d683e50mshe579b860a6a88cap1ebc29jsna3f5e765683f'
RAPIDAPI_HOST = 'google-translate1.p.rapidapi.com'
UPLOAD_FOLDER = '/home/ubuntu/Universal_Translation_Services/uploads'


@app_views.route('/images', methods=['GET'], strict_slashes=False)
def get_images():
    """Get all image translations"""
    """Get image translations"""
    images = storage.all(ImageTranslation)
    return jsonify(images), 200

@app_views.route('/images/<image_id>', methods=['GET'], strict_slashes=False)
def get_image(image_id):
    """Get specific image translations"""
    image = storage.get(ImageTranslation, image_id)
    if image:
        return jsonify(image), 200
    else:
        abort(404, 'Image not found')

@app_views.route('/images', methods=['POST'], strict_slashes=False)
def create_image():
    """Create image translations"""
    if 'file' not in request.files or 'target_lang' not in request.form:
        abort(400, 'Invalid request')

    file = request.files['file']
    target_lang = request.form['target_lang']

    # Process the uploaded image using pytesseract and PIL
    img = Image.open(file)
    input_text = pytesseract.image_to_string(img)
    
    # Perform language detection on the input_text
    translator = Translator(to_lang=target_lang)
    source_lang = translator.detect(input_text)

    translated_text = translator.translate(input_text)
    
    # Store the image details in the database
    image = ImageTranslation(input_text=input_text,
                             source_lang=source_lang,
                             target_lang=target_lang,
                             translated_text=translated_text)
    storage.new(image)
    storage.save()

    # Convert the set to a list for serialization
    image_data = {
        'input_text': image.input_text,
        'source_lang': image.source_lang,
        'target_lang': image.target_lang,
        'translated_text': image.translated_text
    }

    return jsonify(image_data), 201

@app_views.route('/images/<image_id>', methods=['DELETE'], strict_slashes=False)
def delete_image(image_id):
    """Delete stored image translations"""
    image = storage.get(ImageTranslation, image_id)
    if not image:
        abort(404, 'Image not found')

    storage.delete(image)
    storage.save()

    return jsonify({'message': 'Image translations deleted'}), 200
