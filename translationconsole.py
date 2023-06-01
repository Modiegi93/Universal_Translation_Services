#!/usr/bin/python3
"""
Console for the client and the management
"""
import cmd
import requests
import translator
import googletrans
import translator
import pytesseract
import requests
from PIL import Image
from translator import storage
from bs4 import BeautifulSoup
from googletrans import LANGUAGES, Translator
from translator.translation_model import TranslationModel
from translator.text import TextTranslation
from translator.document import DocumentTranslation
from translator.image import ImageTranslation
from translator.website import WebsiteTranslation
from translator.detect_language import DetectLanguage
from translator.language import LanguageSupport
from translator.feedback import FeedBack
from translator.user import User
import shlex
from datetime import datetime


"""classes = {"TranslationModel": TranslationModel,
           "TextTranslation": TextTranslation,
           "DocumentTranslation": DocumentTranslation,
           "ImageTranslation": ImageTranslation,
           "WebsiteTranslation": WebsiteTranslation,
           "DetectLanguage": DetectLanguage,
            "Feedback": FeedBack,
           "LanguageSupport": LanguageSupport}"""


class TranslationServices:
    def __init__(self):
        self.history = []

    def add_translation(self, source_text, translated_text, source_lang, target_lang, timestamp):
        translation = {
            "source_text": source_text,
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "timestamp": timestamp
        }
        self.history.append(translation)

    def get_translation_history(self):
        return self.history

def detect_language(text):
    """Detect the language of the given text"""
    translator = Translator()
    detected_lang = translator.detect(text)
    return detected_lang.lang

def translate_text(text, source_lang, target_lang, translation_history):
    """Translate the given text"""
    translator = Translator()
    if source_lang == 'auto':
        detected_lang = detect_language(text)
        translated = translator.translate(text, dest=target_lang)
        source_lang = detected_lang
    else:
        translated = translator.translate(text, src=source_lang, dest=target_lang)

    translation_history.add_translation(text, translated.text, source_lang, target_lang, datetime.now())
    return translated.text

    translator.storage.reload()
    translator.storage.new(translation)
    translator.storage.save()

def translate_image(image_path, target_lang, translation_history):
    """Translate the text in the given image"""
    try:
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image)
        translated_text = translate_text(extracted_text, "auto", target_lang, translation_history)
        return translated_text
    except FileNotFoundError:
        print("File not found. Please provide a valid image path.")
        return None

    translator.storage.reload()
    translator.storage.new(translation)
    translator.storage.save()

def translate_document(document_path, target_lang, translation_history):
    """Translate the text in the given document"""
    try:
        with open(document_path, 'r') as file:
            text = file.read()
            translated_text = translate_text(text, "auto", target_lang, translation_history)
            return translated_text
    except FileNotFoundError:
        print("File not found. Please provide a valid document path.")
        return None

    translator.storage.reload()
    translator.storage.new(translation)
    translator.storage.save()

def translate_website(website_url, target_lang, translation_history):
    """Translate the text on the given website"""
    try:
        response = requests.get(website_url)
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        translated_text = translate_text(text, "auto", target_lang, translation_history)
        return translated_text
    except requests.exceptions.RequestException:
        print("Error fetching website content. Please check the URL or your internet connection.")
        return None

    translator.storage.reload()
    translator.storage.new(translation)
    translator.storage.save()

if __name__ == "__main__":
    translation_history = TranslationServices()

    while True:
        print("\n--- MENU ---")
        print("1. Translate text")
        print("2. Translate image")
        print("3. Translate document")
        print("4. Translate website")
        print("5. Translation history")
        print("6. List of supported languages")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            source_text = input("Enter the text to translate: ")
            source_lang = input("Enter the source language code (or leave empty for auto-detection): ")
            if not source_lang:
                source_lang = detect_language(source_text)
                print(f"Detected source language: {LANGUAGES[source_lang]}")
            target_lang = input("Enter the target language code: ")
            translated_text = translate_text(source_text, source_lang, target_lang, translation_history)
            print(f"Translated text: {translated_text}")

        elif choice == "2":
            image_path = input("Enter the path to the image file: ")
            target_lang = input("Enter the target language code: ")
            translated_text = translate_image(image_path, target_lang, translation_history)
            if translated_text:
                print(f"Translated text: {translated_text}")

        elif choice == "3":
            document_path = input("Enter the path to the document: ")
            target_lang = input("Enter the target language code: ")
            translated_text = translate_document(document_path, target_lang, translation_history)
            if translated_text:
                print(f"Translated text: {translated_text}")

        elif choice == "4":
            website_url = input("Enter the URL of the website: ")
            target_lang = input("Enter the target language code: ")
            translated_text = translate_website(website_url, target_lang, translation_history)
            if translated_text:
                print(f"Translated text: {translated_text}")

        elif choice == "5":
            print("--- Translation History ---")
            history = translation_history.get_translation_history()
            for idx, translation in enumerate(history, start=1):
                print(f"\nTranslation {idx}:")
                print(f"Source text: {translation['source_text']}")
                print(f"Translated text: {translation['translated_text']}")
                print(f"Source language: {LANGUAGES.get(translation['source_lang'])}")
                print(f"Target language: {LANGUAGES.get(translation['target_lang'])}")
                print(f"Time Stamp: {translation['timestamp']}")


        elif choice == "6":
            print("--- Supported Languages ---")
            for code, lang in LANGUAGES.items():
                print(f"{code}: {lang}")

        elif choice == "7":
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please try again.")

