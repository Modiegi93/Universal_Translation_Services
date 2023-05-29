from datetime import datetime
from translator import storage
from translator.image import ImageTranslation

# Create a new ImageTranslation object
image_translations = ImageTranslation(
    input_file="image.png",
    source_language="en",
    target_language="fr",
    translated_text="image_fr.png",
    created_at=datetime.now(),
    updated_at=datetime.now()
)

# Add the ImageTranslation object to the database
storage.new(image_translations)
storage.save()

# Print the ID of the newly created ImageTranslation object
print("New ImageTranslation ID:", image_translations.id)
