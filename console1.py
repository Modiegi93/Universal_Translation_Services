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


classes = {"TranslationModel": TranslationModel,
           "TextTranslation": TextTranslation,
           "DocumentTranslation": DocumentTranslation,
           "ImageTranslation": ImageTranslation,
           "WebsiteTranslation": WebsiteTranslation,
           "DetectLanguage": DetectLanguage,
            "Feedback": FeedBack,
           "LanguageSupport": LanguageSupport}


class TranslatorConsole(cmd.Cmd):
    intro = "Welcome to Translation Console! Enter a command or 'help' for assistance."
    prompt = "Translation Console> "

    def __init__(self):
        super().__init__()
        self.translation_history = TranslationHistory()
        self.text_translations = TextTranslations()
        self.document_translations = DocumentTranslations()
        self.image_translations = ImageTranslations()
        self.website_translations = WebsiteTranslations()
        self.detect_language = DetectLanguage()
        self.language_supported = LanguageSupport()
        self.feedback_translations = FeedBack()

    def do_translate(self, arg):
        """Translate the given text"""
        # Extract the source language, target language, and text from the argument
        args = arg.split()
        if len(args) < 3:
            print("Invalid syntax. Usage: translate <source_lang> <target_lang> <text>")
            return

        source_lang = args[0]
        target_lang = args[1]
        text = " ".join(args[2:])

        # Call the appropriate translation method based on the text type
        if is_text_type(text):
            translated_text = self.text_translations.translate_text(text,
                                                                    source_lang, target_lang)
            print("Translated text: {}".format(translated_text))
        elif is_document_type(text):
            translated_doc = self.document_translations.translate_document(text,
                                                                           source_lang, target_lang)
            print("Translated document: {}".format(translated_doc))
        elif is_image_type(text):
            translated_image = self.image_translations.translate_image(text, source_lang, target_lang)
            print("Translated image: {}".format(translated_image))
        elif is_website_type(text):
            translated_website = self.website_translations.translate_website(text, source_lang, target_lang)
            print("Translated website: {}".format(translated_website))
        else:
            print("Invalid text type. Supported types: text, document, image, website")

    def do_detectlanguage(self, arg):
        """Detect the language of the given text"""
        text = arg.strip()
        if text:
            detected_language = self.text_translations.detect_language(text)
            print("Detected language: {}".format(detected_language))
        else:
            print("Please provide text to detect the language.")

    def do_languagesupported(self, arg):
        """List all supported languages"""
        supported_languages = self.text_translations.get_supported_languages()
        print("Supported languages:")
        for language in supported_languages:
            print("- {}".format(language))

    def do_translatedhistory(self, arg):
        """Display the translation history"""
        translations = self.text_translations.storage.get(translation_history())
        if translations:
            print("Translation history:")
            for translation in translations:
                print("- Input: {}".format(translation.storage.get(input_text)))
                print("  Translated: {}".format(translation.storage.get(translated_text)))
                print("  Source language: {}".format(translation.storage.get(source_lang)))
                print("  Target language: {}".format(translation.storage.get(target_lang)))
                print("  Translation time: {}".format(translation.storage.get(created_at)))
                print()
        else:
            print("No translation history available.")

    def do_clearhistory(self, arg):
        """Clear the translation history"""
        self.text_translations.storage.delete(translation_history())
        print("Translation history cleared.")

    def is_text_type(text):
        # Check if the text is of type text
        pass

    def is_document_type(text):
        # Check if the text is of type document
        pass

    def is_image_type(text):
        # Check if the text is of type image
        pass

    def is_website_type(text):
        # Check if the text is of type website
        pass

    def do_translate_text(self, arg):
        """Translate the given text"""
        # Parse the input arguments
        args = arg.split()
        if len(args) != 3:
            print("Invalid arguments. Usage: translate_text <text> <source_lang> <target_lang>")
            return

        text, source_lang, target_lang = args
        translated_text = translate_text(text, source_lang, target_lang, self.translation_history)
        if translated_text:
            print(f"Translated text: {translated_text}")

    def do_translate_image(self, arg):
        """Translate text in the given image"""
        # Parse the input arguments
        args = arg.split()
        if len(args) != 2:
            print("Invalid arguments. Usage: translate_image <image_path> <target_lang>")
            return

        image_path, target_lang = args
        translated_text = translate_image(image_path, target_lang, self.translation_history)
        if translated_text:
            print(f"Translated text: {translated_text}")

    def do_translate_document(self, arg):
        """Translate text in the given document"""
        # Parse the input arguments
        args = arg.split()
        if len(args) != 2:
            print("Invalid arguments. Usage: translate_document <document_path> <target_lang>")
            return

        document_path, target_lang = args
        translated_text = translate_document(document_path, target_lang, self.translation_history)
        if translated_text:
            print(f"Translated text: {translated_text}")

    def do_translate_website(self, arg):
        """Translate text on the given website"""
        # Parse the input arguments
        args = arg.split()
        if len(args) != 2:
            print("Invalid arguments. Usage: translate_website <website_url> <target_lang>")
            return

        website_url, target_lang = args
        translate_website(website_url, target_lang, self.translation_history)

    def do_translation_history(self, arg):
        """View the translation history"""
        history = self.translation_history.get_translation_history()
        for idx, translation in enumerate(history, start=1):
            print(f"\nTranslation {idx}:")
            print(f"Source text: {translation['source_text']}")
            print(f"Translated text: {translation['translated_text']}")
            print(f"Source language: {LANGUAGES[translation['source_lang']]}")
            print(f"Target language: {LANGUAGES[translation['target_lang']]}")

    def do_languagesupported(self, arg):
        """List supported languages"""
        supported_languages = self.text_translations.get_supported_languages()
        print("--- Supported Languages ---")
        for language in supported_languages:
            print("- {}".format(language))

    def do_feedback(self, arg):
        """Provide feedback on the translation service"""
        feedback = arg.strip()
        if feedback:
            self.feedback_translations.add_feedback(feedback)
            print("Thank you for your feedback!")
        else:
            print("Please provide feedback.")

    def do_help(self, arg):
        """Display available commands and their descriptions"""
        if arg:
            # Show detailed help for a specific command
            try:
                doc = getattr(self, "do_" + arg).__doc__
                if doc:
                    print(doc)
                else:
                    print("No help available for '{}'".format(arg))
            except AttributeError:
                print("No help available for '{}'".format(arg))
        else:
            # Show general help
            print("Available commands:")
            command_names = [cmd for cmd in self.get_names() if cmd.startswith("do_")]
            for command_name in command_names:
                command = command_name[3:]  # Remove the "do_" prefix
                doc = getattr(self, command_name).__doc__
                if doc:
                    print("- {}: {}".format(command, doc))

    def do_quit(self, arg):
        """Exit the program"""
        print("Exiting the program...")
        return True

    def emptyline(self):
        """Ignore empty lines"""
        pass


if __name__ == "__main__":
    console = TranslationConsole()
    console.cmdloop()

class TranslationHistory:
    def __init__(self):
        self.history = []

    def add_translation(self, source_text, translated_text, source_lang, target_lang):
        translation = {
            "source_text": source_text,
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang
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
        translated = translator.translate(text, src=source_lang, dest=target_lang)
        translation_history.add_translation(text, translated.text, source_lang, target_lang)
        return translated.text

    def translate_image(image_path, target_lang, translation_history):
        """Translate the text in the given image"""
        try:
            image = Image.open(image_path)
            extracted_text = pytesseract.image_to_string(image)
            translated_text = translate_text(extracted_text, "auto", target_lang,
                                             translation_history)
            return translated_text
        except FileNotFoundError:
            print("File not found. Please provide a valid image path.")
            return None

    def translate_document(document_path, target_lang, translation_history):
        """Translate the text in the given document"""
        try:
            with open(document_path, 'r') as file:
                text = file.read()
                translated_text = translate_text(text, "auto", target_lang,
                                                 translation_history)
                return translated_text
        except FileNotFoundError:
            print("File not found. Please provide a valid document path.")
            return None

    def translate_website(website_url, target_lang, translation_history):
        """Translate the text on the given website"""
        try:
            # Fetch the HTML content of the website
            response = requests.get(website_url)
            html_content = response.text

            # Create a BeautifulSoup object to parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all text elements on the website
            text_elements = soup.find_all(text=True)

            # Translate each text element and replace the original text with the translated text
            translator = Translator()
            for element in text_elements:
                source_text = element.strip()
                if source_text:
                    source_lang = translator.detect(source_text).lang
                    translated_text = translate_text(source_text, source_lang,
                                                     target_lang, translation_history)
                    element.replace_with(translated_text)

            # Print the translated website content
            print("--- Translated Website ---")
            print(soup)

        except requests.exceptions.RequestException as e:
            print("An error occurred while fetching the website:", e)
    

        print(f"Translating website: {website_url}")
        print(f"Target Language: {LANGUAGES[target_lang]}")

if __name__ == "__main__":
    translation_history = TranslationHistory()

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
            translate_website(website_url, target_lang, translation_history)

        elif choice == "5":
            print("--- Translation History ---")
            history = translation_history.get_translation_history()
            for idx, translation in enumerate(history, start=1):
                print(f"\nTranslation {idx}:")
                print(f"Source text: {translation['source_text']}")
                print(f"Translated text: {translation['translated_text']}")
                print(f"Source language: {LANGUAGES[translation['source_lang']]}")
                print(f"Target language: {LANGUAGES[translation['target_lang']]}")

        elif choice == "6":
            print("--- Supported Languages ---")
            for code, lang in LANGUAGES.items():
                print(f"{code}: {lang}")

        elif choice == "7":
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please try again.")
