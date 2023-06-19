#!/usr/bin/python3
"""
Class TextTranslations
"""
import json
import uuid
import translator
from translator.translation_model import TranslationModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Text


class Settings(TranslationModel, Base):

    if translator.storage_type == "db":
        __tablename__ = "text_translations"
        id = Column(String(50), primary_key=True)
        target_languages = Column(String(100))
        default_language = Column(String(100))

    else:
        id = ""
        target_languages = ""
        default_language = ""

    def __init__(self, *args, **kwargs):
        """initializes all translations"""
        super().__init__(*args, **kwargs)
