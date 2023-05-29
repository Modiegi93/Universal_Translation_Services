#!/usr/bin/python3
from datetime import datetime
from translator import storage
from translator.document import DocumentTranslation

# Create a new DocumentTranslation object
document_translations = DocumentTranslation(
    input_file="document.txt",
    source_language="en",
    target_language="fr",
    translated_text="document_fr.txt",
    created_at=datetime.now(),
    updated_at=datetime.now()
)

# Add the DocumentTranslation object to the database
storage.new(document_translations)
storage.save()

# Print the ID of the newly created DocumentTranslation object
print("New DocumentTranslation ID:", document_translations.id)
