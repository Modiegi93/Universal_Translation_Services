#!/usr/bin/python3
from datetime import datetime
import translator
from translator import storage
from translator.language import LanguageSupport

language_supported = LanguageSupport(
    language_code="en",
    language_name="English",
    created_at=datetime.now(),
    updated_at=datetime.now()
)

# Add the LanguageSupport object to the database
storage.new(language_supported)
storage.save()

# Print the ID of the newly created LanguageSupport object
print("New LanguageSupport ID:", language_supported.id)
