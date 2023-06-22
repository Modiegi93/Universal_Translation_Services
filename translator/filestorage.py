#!/usr/bin/python3
import json


# Update the TranslationServices class
class FileStorage:
    def __init__(self):
        self.history = []
        self.json_file = 'translations.json'

        # Load existing translations from JSON file
        self.load_translations()

    def add_translation(self, source_text, translated_text, source_lang,
                        target_lang, timestamp):
        translation = {
            "source_text": source_text,
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "timestamp": str(timestamp)
        }
        self.history.append(translation)
        self.save_translations()

    def get_translation_history(self):
        return self.history

    def save_translations(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.history, file)

    def load_translations(self):
        try:
            with open(self.json_file, 'r') as file:
                self.history = json.load(file)
        except FileNotFoundError:
            self.history = []

# Usage example
translation_history = TranslationServices()

# Add translation
translation_history.add_translation('Hello', 'Hola', 'en', 'es', datetime.now())

# Get translation history
history = translation_history.get_translation_history()
for translation in history:
    source_text = translation['source_text']
    translated_text = translation['translated_text']
    source_lang = translation['source_lang']
    target_lang = translation['target_lang']
    timestamp = datetime.fromisoformat(translation['timestamp'])
    print(f"Source: {source_text}, Translated: {translated_text}, Source Lang: {source_lang}, Target Lang: {target_lang}, Timestamp: {timestamp}")
