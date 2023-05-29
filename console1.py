#!/usr/bin/python3
"""
Console for the client and the management
"""
import cmd
import requests
import translator
import googletrans
#from google.cloud import vision
import translate
from translate import Translator
from bs4 import BeautifulSoup
#from google.cloud import translate_v2 as translate
#from google.cloud import translate_v3beta1 as translate_v3
#from googletrans import LANGUAGES, Translator
from translator.all_translations import AllTranslations
from translator.list_languages import LanguageSupport
from translator.feedback import FeedBack
import shlex
from datetime import datetime

#translator = googletrans.Translator()
#vision_client = vision.ImageAnnotatorClient()
#translator_v2 = translate.Client()
#translator_v3 = translate_v3.TranslationServiceClient()
classes = {"All_Translations": AllTranslations, "Feedback": FeedBack,
           "Languages": LanguageSupport}


class TranslatorConsole(cmd.Cmd):
    """Translator web service console"""
    
    prompt = 'Translation > '

    def do_translate_text(self, args):
        """Translate text"""
        input_text = input("Enter the text to translate: ")
        source_lang = input("Enter the source language: ").lower()
        target_lang = input("Enter the target language: ").lower()

        translated_text = self.translate_text(input_text, source_lang,
                                              target_lang)
        print("Translated Text:", translated_text)

    def do_translate_image(self, arg):
        """Translate image"""
        image_path = input("Enter the path to the image: ")
        source_lang = input("Enter the source language: ")
        target_lang = input("Enter the target language: ")

        translated_text = self.translate_image(image_path, source_lang,
                                               target_lang)
        print("Translated Text:")
        print(translated_text)

    def do_translate_document(self, arg):
        """Translate document"""
        document_path = input("Enter the path to the document: ")
        source_lang = input("Enter the source language: ")
        target_lang = input("Enter the target language: ")

        translated_document = self.translate_document(document_path,
                                                      source_lang, target_lang)
        print("Translated Document:")
        print(translated_document)

    def do_translate_website(self, arg):
        """Translate website"""
        website_url = input("Enter the website URL: ")
        source_lang = input("Enter the source language: ")
        target_lang = input("Enter the target language: ")

        translated_website = self.translate_website(website_url, source_lang,
                                                    target_lang)
        print("Translated Website:")
        print(translated_website)

    def do_detect_language(self, arg):
        """Detect language"""
        text = input("Enter the text to detect language: ")

        detected_language = self.detect_language(text)
        print("Detected Language:", detected_language)

    def do_get_supported_languages(self, arg):
        """Get supported languages"""
        supported_languages = self.get_supported_languages()
        print("Supported Languages:")
        for lang, desc in supported_languages.items():
            print(f"{lang}: {desc}")

    def do_exit(self, arg):
        """Exit the program"""
        print("Exiting...")
        return True

    def translate_text(self, text, source_lang, target_lang):
        """Translate the given text"""
        translator = Translator(from_lang=source_lang, to_lang=target_lang)
        translated_text = translator.translate(text)
        return translated_text

    """def translate_image(self, image_path, source_lang, target_lang):
        #Translate the text in the given image
        with open(image_path, 'rb') as image_file:
        content = image_file.read()

        image = vision.Image(content=content)
        response = vision_client.text_detection(image=image)
        text_annotations = response.text_annotations

        if text_annotations:
            text = text_annotations[0].description
            return translate_text(text, source_lang, target_lang)
        else:
            return "No text found in the image" """

    def translate_document(self, document_path, source_lang, target_lang):
        """Translate the text in the given document"""
        with open(document_path, 'r') as document_file:
            text = document_file.read()

        translation = translator.translate(text, src=source_lang,
                                           dest=target_lang)
        return translation.text

    def translate_website(self, website_url, source_lang, target_lang):
        """Translate the text on the given website"""
        # Get the content of the website
        response = requests.get(website_url)
        content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')

        # Find all text elements on the website
        text_elements = soup.find_all(text=True)

        # Translate each text element
        for element in text_elements:
            translated_text = self.translate_text(element, source_lang,
                                                  target_lang)
            element.replace_with(translated_text)

        # Return the translated website
        return str(soup)

    def detect_language(self, text):
        """Detect the language of the given text using googletrans"""
        detection = translator.detect(text)
        return detection.lang

    def get_supported_languages(self):
        """Get the list of supported languages for translation"""
        return googletrans.LANGUAGES


if __name__ == '__main__':
    TranslatorConsole().cmdloop()
