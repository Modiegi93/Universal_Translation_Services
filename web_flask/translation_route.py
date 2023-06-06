#!/usr/bin/python3
"""
Translation route
"""
import translator
import requests
import uuid
import json
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template
from googletrans import Translator, LANGUAGES
from os import getenv
from translator import storage
from translator.translation_model import TranslationModel, Base
from translator.text import TextTranslation
from translator.document import DocumentTranslation
from translator.image import ImageTranslation
from translator.website import WebsiteTranslation
from translator.detect_language import DetectLanguage
from translator.language import LanguageSupport
from translator.feedback import FeedBack
from translator.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)

translator = Translator()


@app.route('/translations')
def translations_page():
    """Return an html template or JSON response"""
    return render_template('translations.html')

@app.route('/translations/text', methods=['POST'])
def translate_text():
# Get the source text and target language from the form
    input_text = request.form.get('input_text')
    target_language = request.form.get('target_language')

    # Perform the translation using the googletrans library
    translator = Translator()
    translation = translator.translate(source_text, dest=target_language).text

    # Store the translation in the database and file storage
    new_translation = TextTranslation(text=input_text,
                                       source_language='auto',
                                       target_language=target_language,
                                       translated_text=translation)
    storage.new(new_translation)
    storage.save()

    return render_template('translations.html', translation=translation)


@app.route('/translations/<language_supported>')
def get_supported_languages(language_supported):
    if language_supported == 'all':
        supported_languages = LANGUAGES
    else:
        # Filter the supported languages based on the provided language code
        supported_languages = {code: name for code, name in LANGUAGES.items()
                               if code.startswith(language_supported)}
        
        storage.new(supported_languages)
        storage.save()

    return render_template('translations.html',
                           supported_languages=supported_languages)

@app.route('/translations/detect_language', methods=['POST'])
def detect_language():
    # Get the text to detect language from the request data
    text_to_detect = request.json['text']

    # Perform language detection using Google Translate
    detected_language = detect_languages(text_to_detect)

    storage.new(detected_language)
    storage.save()

    return jsonify({'detected_language': detected_language})

def detect_languages(text):
    # Create an instance of the Translator class
    translator = Translator()

    # Use the detect() method to detect the language
    detected_language = translator.detect(text).lang

    return detected_language

@app.route('/feedback', methods=['POST'])
def receive_feedback():
    feedback = request.json.get('feedback')

    # Process and store the feedback in your database or perform
    any desired actions

    return jsonify({'message': 'Feedback received'})

@app.route('/')
def index():
    return render_template('translations.html')

@app.route('/translations/text', methods=['GET', 'POST'])
def translate_text():
    if request.method == 'POST':
        text_to_translate = request.form.get('textToTranslate')
        translator = Translator()
        translated_text = translator.translate(text_to_translate)

        storage.new(translated_text)
        storage.save()

        return {'translated_text': translated_text.text}
    
    return render_template('translations.html')

@app.route('/translations/document', methods=['POST'])
def translate_document():
    # Get the uploaded document from the request
    document = request.files['document-input']

    # Read the contents of the document
    document_text = document.read()

    # Perform the translation using Googletrans
    translator = Translator()
    translated_text = translator.translate(document_text)

    storage.new(translated_text)
    storage.save()
    
    # Render the template with the translated text
    return render_template('translations.html',
                           translated_text=translated_text.text)

@app.route('/translations/image', methods=['POST'])
def translate_image():
    file = request.files['image-input']
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    
    translator = Translator()
    translation = translator.translate(text, dest='en')
   
    storage.new(translation)
    storage.save()

    return translation.text

@app.route('/translations/website', methods=['POST'])
def translate_website():
    url = request.form.get('website-input')
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    
    translator = Translator()
    translation = translator.translate(text, dest='en')
    
    storage.new(translation)
    storage.save()

    return translation.text

@app.route('/translations/history')
def translation_history():
    # Retrieve translations from the database
    translations = TranslationModel.query.all()

    # Render the template with the translations data
    return render_template('translation_history.html',
                           translations=translations)

@app.teardown_appcontext
def close_session(exception):
    """Remove the db session or save file"""
    storage.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
