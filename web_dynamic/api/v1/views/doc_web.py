from flask import Flask, request, jsonify, abort
from googletrans import Translator
from api.v1.views import app_views
from translator import storage
from translator.document import DocumentTranslation
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup
import requests

translator = Translator()

@app_views.route('/imagez', methods=['POST'], strict_slashes=False)
def trans_image():
    """Create image translations"""
    try:
        # Check if an image file is included in the request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file found'})

        # Read the image file
        image_file = request.files['image']
        image = Image.open(image_file)

        # Perform OCR to extract the text from the image
        extracted_text = pytesseract.image_to_string(image)

        # Get the source and target languages from the request
        source_language = request.form['source_language']
        target_language = request.form['target_language']

        # Translate the extracted text
        translated_text = translator.translate(extracted_text, src=source_language,
                                               dest=target_language).text

        translation = ImageTranslation(input_text=image_file, source_lang=source-language,
                                       target_lang=target_language,
                                       translated_text=translated_text)

        storage.new(translation)
        storage.save()

        return jsonify({'translated_text': translated_text})

@app_views.route('/websitez', methods=['POST'], strict_slashes=False)
def trans_web():
    """Create website translations"""
     # Get the website URL from the request
            url = request.json['url']

            # Make a GET request to the website
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code != 200:
                return jsonify({'error': 'Failed to fetch the website content'})

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the text content from the website
            text = soup.get_text()

            # Translate the text to the target language
            translated_text = translator.translate(text, src=source_language,
                    dest=target_language).text

            # Save the translation to the WebsiteTranslation table
            translation = WebsiteTranslation(input_text=url, source_language=source_lang,
                                             target_language=target_lang,
                                             translated_text=translated_text)
            storage.new(translation)
            storage.save()

        else:
            return jsonify({'error': 'Invalid translation type'})

        return jsonify({'message': 'Translation saved successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

