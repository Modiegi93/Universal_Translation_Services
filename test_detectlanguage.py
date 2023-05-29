#!/usr/bin/python3
from datetime import datetime
import translator
from translator import storage
from translator.detect_language import DetectLanguage

detect_languages = DetectLanguage(
    input_text="Hello, world!",
    detected_lang="en",
    created_at=datetime.now(),
    updated_at=datetime.now()
    )

storage.new(detect_languages)
storage.save()

print("New DetectLanguage ID:", detect_languages.id)
