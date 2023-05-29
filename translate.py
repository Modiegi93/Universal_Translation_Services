#!/usr/bin/python3

import googletrans
from googletrans import Translator, LANGUAGES
#from PIL import image
#from google.cloud import vision
#from google.cloud import translate_v2 as translate
import requests
from bs4 import BeautifulSoup


def translateText(inputText, sourceLang, targetLang):
        """Create a translator object"""
        translator = Translator(service_urls=['translate.google.com'])

        """Check if the source and target languages are supported"""
        if sourceLang not in LANGUAGES or targetLang not in LANGUAGES:
            raise ValueError("Language not supported")

        """ Translate the input text"""
        translation = translator.translate(inputText, src=sourceLang,
                                           dest=targetLang)

        """Extract the translated text"""
        translatedText = translation.text

        """Create a dictionary to store the translation data"""
        translationData = {
                "inputText": inputText,
                "sourceLang": sourceLang,
                "targetLang": targetLang,
                "translatedText": translatedText
                }

        """Save the translation data to a JSON file"""
        with open("translated_text.json", "w") as file:
            json.dump(translationData, file, indent=4)

        return translatedText

def translateDocument(inputFile, sourceLang, targetLang):
    """Read the document file"""
    with open(inputFile, 'r') as file:
        document_content = file.read()

    """Initialize the translator"""
    translator = Translator()

    """Detect the language of the document"""
    detected_lang  = translator.detect(document_content).lang


    """Translate the document if detected lang matches the source lang"""
    if detected_lang == sourceLang:
            translated_content = translator.translate(document_content,
                                                      src=sourceLang,
                                                      dest=targetLang).text
    else:
        translated_content = "Source language does not match the detected language of the document."

    return translated_content

"""def translateImage(inputImage, sourceLang, targetLang):
    #Initialize the Vision and Translation clients
    vision_client = vision.ImageAnnotatorClient()
    translate_client = translate.Client()

    #Process the image
    if isinstance(inputImage, str):
        #If the input is a file path, open the image file
        with Image.open(inputImage) as image:
            image_content = image.tobytes()
    else:
        #If the input is already an image object, convert it to bytes
        image_content = inputImage.tobytes()

        #Perform text recognition on the image
        image = vision.Image(content=image_content)
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations

        #Extract the detected text
        detected_text = texts[0].description if texts else ''


        #Translate the detected text
        translated_text = translate_client.translate(detected_text,
                                                     source_language=sourceLang,
                                                     target_language=targetLang)

        return translated_text['translatedText']"""

def translateWebsite(inputUrl, sourceLang, targetLang):
    """Retrieve the HTML content of the website"""
    response = requests.get(inputUrl)
    html_content = response.text

    """Parse the HTML using BeautifulSoup"""
    soup = BeautifulSoup(html_content, 'html.parser')

    """Find all text elements in the HTML"""
    text_elements = soup.find_all(text=True)

    """Translate each text element"""
    translator = Translator()
    translated_content = []
    for element in text_elements:
        translated_text = translator.translate(element, src=sourceLang,
                                               dest=targetLang).text
    translated_content.append(translated_text)

    """Update the text elements with the translated content"""
    for i, element in enumerate(text_elements):
        element.string = translated_content[i]

    """Return the translated HTML"""
    translated_html = soup.prettify()
    return translated_html

def detectLanguage(inputText):
    translator = Translator()
    detected_lang = translator.detect(inputText).lang

    return detected_lang

def getSupportedLanguages():
    supported_languages = []

    for lang_code, lang_name in LANGUAGES.items():
        supported_languages.append({'code': lang_code, 'language': lang_name})

    return supported_languages
