#!/usr/bin/python3
from datetime import datetime
from translator import storage
from translator.text import TextTranslation

# Create a new TextTranslation object
text_translations = TextTranslation(
    input_text="Hello, world!",
    source_lang="en",
    target_lang="fr",
    translated_text="Bonjour, le monde!",
    created_at=datetime.now(),
    updated_at=datetime.now()
)

# Add the TextTranslation object to the database
storage.new(text_translations)
storage.save()

# Print the ID of the newly created TextTranslation object
print("New TextTranslation ID:", text_translations.id)
