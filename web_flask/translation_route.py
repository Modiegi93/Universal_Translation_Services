#!/usr/bin/python3
"""Translation web framework"""
import translate
import translator
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template
from googletrans import Translator
from translate import Translator
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

@app.route('/translations', methods=['GET'])
def translations_page():
    """Return an html template or JSON response"""
    return render_template('translations.html')

@app.route('/translations/text', methods=['POST'])
def translate_text():
    """Retrieve necessary data from the request payload"""
    data = request.json
    texts = data.get('texts')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')

    translated_texts = []

    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    
    for text in texts:
        translated_text = translator.translate(text)
        translation = TextTranslation(input_text=text,
                                      translated_text=translated_text)
        translated_texts.append(translated_text)

    return render_template('translations.html', texts=texts,
                           translated_texts=translated_texts)

@app.route('/translations/document', methods=['POST'])
def translate_document():
    """Return the translated text from a file"""
    file = request.files['file']
    source_lang = request.form.get('source_lang')
    target_lang = request.form.get('target_lang')

    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    translated_file = f"translated_{file.filename}"

    translated_file_path = f"/home/ubuntu/Universal_Language_Translation/{translated_file}"
    file.save(translated_file_path)

    translated_document = translator.translate_file(translated_file_path)

    return render_template('translations.html', Query_name="DocumentTranslation",
                           translated_document=translated_document)


@app.route('/translations/image', methods=['POST'])
def translate_image():
    """Return the translated image file"""
    file = request.files['file']
    source_lang = request.form.get('source_lang')
    target_lang = request.form.get('target_lang')

    translated_image = translate_image_file(file, source_lang, target_lang)

    translation = ImageTranslation(source_lang=source_lang, target_lang=target_lang,
                                   translated_image=translated_image)
    storage.new(translation)
    storage.save()

    return render_template('translations.html', 
                           translated_image=translated_image)

def translate_image_file(file, source_lang, target_lang):
    """Translate the text in the given image"""
    vision_client = vision.ImageAnnotatorClient()
    image_content = file.read()

    image = vision.Image(content=image_content)

    response = vision_client.text_detection(image=image)
    text_annotations = response.text_annotations

    if text_annotations:
        text = text_annotations[0].description
        translated_text = translate_text(text, source_lang, target_lang)
        return translated_text
    else:
        return "No text found in the image"

@app.route('/translations/website', methods=['POST'])
def translate_website():
    """Return the translated website"""
    website_url = request.json.get('website_url')
    source_lang = request.json.get('source_lang')
    target_lang = request.json.get('target_lang')

    response = requests.get(website_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    text_elements = soup.find_all(text=True)

    translated_elements = []
    for element in text_elements:
        translated_text = translate_text(element, source_lang, target_lang)
        translated_elements.append(translated_text)

    for i, element in enumerate(text_elements):
        element.string = translated_elements[i]

    translated_html = str(soup)

    translation = WebsiteTranslation(website_url=html_content, 
                                     translated_website=translated_html)
    
    storage.new(translation)
    storage.save()

    return render_template('translations.html',
                           translated_html=translated_html)


@app.route('/translations/detect-language', methods=['POST'])
def detect_language():
    """Detect the language of the input text"""
    input_text = request.json.get('text')

    detected_language = detect_language(input_text)

    detection = DetectedLanguage(input_text=input_text,
                                 detected_language=detected_language)
    return render_template('translations.html',
                           detect_language=detect_language)

def detected_language(text):
    """Detect the language of the given text"""
    translator = Translator(to_lang='en', from_lang='auto')
    detected_language = translator.translate(text).split(' ')[-1]
    return detected_language

@app.route('/translations/languages', methods=['GET'])
def get_supported_languages():
    """Get the list of supported languages for translation"""
    populate_supported_languages()
    supported_languages = LanguageSupport.storage.all("Languages").values
    languages = [{'code': lang.code, 'language': lang.language} 
                 for lang in supported_languages]
    return render_template('translations.html',
                           supported_languages=supported_languages)

def populate_supported_languages():
    """Populate the supported languages in the database"""
    translator = Translator(to_lang='en')
    languages = translator.languages.keys()

    for code in languages:
        language = translator.languages[code]
        supported_language = LanguageSupport(code=code, language=language)
        storage.new(supported_language)
    storage.save()

@app.route('/translations/feedback', methods=['POST'])
def submit_feedback():
    """Submit translation feedback"""
    id = request.json.get('translation_id')
    input_text = request.json.get('input_text')

    feedback = FeedBack(id=id, input_text=input_text)
    storage.new(feedback)
    storage.save()

    return render_template('feedback_success.html')

@app.teardown_appcontext
def close_session(exception):
    """Remove the db session or save file"""
    storage.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")

