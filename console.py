#!/usr/bin/python3
"""
Console for the client and the management
"""
import cmd
import translator
from translator import storage
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
import translate


classes = {"TranslationModel": TranslationModel,
           "TextTranslation": TextTranslation,
           "DocumentTranslation": DocumentTranslation,
           "ImageTranslation": ImageTranslation,
           "WebsiteTranslation": WebsiteTranslation,
           "User": User, "DetectLanguage": DetectLanguage,
           "Feedback": FeedBack, "LanguageSupport": LanguageSupport}


class TranslatorConsole(cmd.Cmd):
    """Translator web service console"""

    prompt = "Translation: "

    def do_EOF(self, line):
        """Handle the End-of-File signal"""
        return True

    def do_create(self, arg):
        """Create a new translation object"""
        args = arg.split()
        if len(args) == 0:
            print("** Object type missing **")
            return

        obj_type = args[0]
        if obj_type == 'text':
            if len(args) < 4:
                print("** Missing required arguments **")
                print("Usage: create text <input_text> <source_lang> <target_lang>")
                return
            input_text = args[1]
            source_lang = args[2]
            target_lang = args[3]

            translation = TextTranslation(input_text, source_lang, target_lang)
            storage.new(translation)
            print("Text translation created successfully.")
            print(translation)

        elif obj_type == 'document':
            if len(args) < 4:
                print("** Missing required arguments **")
                print("Usage: create document <input_file> <source_lang> <target_lang>")
                return
            input_file = args[1]
            source_lang = args[2]
            target_lang = args[3]

            translation = DocumentTranslation(input_file, source_lang, target_lang)
            storage.new(translation)
            print("Document translation created successfully.")
            print(translation)

        elif obj_type == 'image':
            if len(args) < 4:
                print("** Missing required arguments **")
                print("Usage: create image <input_file> <source_lang> <target_lang>")
                return
            input_file = args[1]
            source_lang = args[2]
            target_lang = args[3]

            translation = ImageTranslation(input_file, source_lang, target_lang)
            storage.new(translation)
            print("Image translation created successfully.")
            print(translation)

        elif obj_type == 'website':
            if len(args) < 4:
                print("** Missing required arguments **")
                print("Usage: create website <website_url> <source_lang> <target_lang>")
                return
            website_url = args[1]
            source_lang = args[2]
            target_lang = args[3]

            translation = WebsiteTranslation(website_url, source_lang, target_lang)
            storage.new(translation)
            print("Website translation created successfully.")
            print(translation)

        elif obj_type == 'detect_language':
            if len(args) < 2:
                print("**  Missing required arguments **")
                print("Usage: create detect_language <input_text>")
                return
            input_text = args[1]

            translation = DetectLanguage(input_text)
            storage.new(translation)
            print("Detect language created successfully.")
            print(translation)

        elif obj_type == 'user':
            if len(args) < 5:
                print("**  Missing required arguments **")
                print("Usage: create user <email> <full_name> <password>")
                return
            email = args[1]
            full_name = args[2]
            password = [3]

            translation = User(email, full_name, password)
            storage.new(translation)
            print("User created successfully.")
            print(translation)


        else:
            print("** Invalid object type **")

    def do_show(self, arg):
        """Show details of a translation object"""
        args = arg.split()
        if len(args) != 2:
            print("** Usage: show <object_type> <object_id> **")
            return

        obj_type = args[0]
        obj_id = args[1]

        if obj_type == 'text':
            translation = storage.get(TextTranslation, obj_id)
        elif obj_type == 'document':
            translation = storage.get(DocumentTranslation, obj_id)
        elif obj_type == 'image':
            translation = storage.get(ImageTranslation, obj_id)
        elif obj_type == 'website':
            translation = storage.get(WebsiteTranslation, obj_id)
        elif obj_type == 'detect_language':
            translation = storage.get(DetectLanguage, obj_id)

        else:
            print("** Invalid object type **")
            return

        if translation:
            print(translation)
        else:
            print("** Translation object not found **")

    def do_delete(self, arg):
        """Delete a translation object"""
        args = arg.split()
        if len(args) != 2:
            print("** Usage: delete <object_type> <object_id> **")
            return

        obj_type = args[0]
        obj_id = args[1]

        if obj_type == 'text':
            deleted = storage.delete(TextTranslation, obj_id)
        elif obj_type == 'document':
            deleted = storage.delete(DocumentTranslation, obj_id)
        elif obj_type == 'image':
            deleted = storage.delete(ImageTranslation, obj_id)
        elif obj_type == 'website':
            deleted = storage.delete(WebsiteTranslation, obj_id)
        elif obj_type == 'detect_language':
            deleted = storage.delete(DetectLanguage, obj_id)

        else:
            print("** Invalid object type **")
            return

        if deleted:
            print("Translation object deleted successfully.")
        else:
            print("** Translation object not found **")

    def do_feedback(self, arg):
        """Submit user feedback"""
        args = arg.split()
        if len(args) < 2:
            print("** Missing required arguments **")
            print("Usage: feedback <translation_id> <message>")
            return

        translation_id = args[0]
        message = ' '.join(args[1:])

        feedback = FeedBack(translation_id, message)
        storage.new(feedback)
        print("Feedback submitted successfully.")

    def do_supported_languages(self, arg):
        """Get supported languages"""
        supported_languages = LanguageSupport.getSupportedLanguages()
        if supported_languages:
            print("Supported Languages:")
            for lang in supported_languages:
                print(f"- {lang}")
        else:
            print("** Unable to retrieve supported languages **")

    def do_quit(self, arg):
        """Quit the console"""
        return True


if __name__ == '__main__':
    TranslatorConsole().cmdloop()
