#!/usr/bin/python3
from datetime import datetime
from translator import storage
from translator.website import WebsiteTranslation

# Create a new WebsiteTranslation object
website_translations = WebsiteTranslation(
    input_text="https://example.com",
    source_lang="en",
    target_lang="fr",
    translated_text="https://example.com/fr",
    created_at=datetime.now(),
    updated_at=datetime.now()
)

# Add the WebsiteTranslation object to the database
storage.new(website_translations)
storage.save()

# Print the ID of the newly created WebsiteTranslation object
print("New WebsiteTranslation ID:", website_translations.id)
