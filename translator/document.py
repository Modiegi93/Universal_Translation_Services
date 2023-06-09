#!/usr/bin/python3
"""
Class DocumentTranslation
"""
import json
import translator
import uuid
from translator.translation_model import TranslationModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Text


class DocumentTranslation(TranslationModel, Base):

    if translator.storage_type == "db":
        __tablename__ = "document_translations"
        id = Column(String(60), primary_key=True)
        input_text = Column(Text, nullable=False)
        source_lang = Column(String(50), nullable=False)
        target_lang = Column(String(50), nullable=False)
        translated_text = Column(Text, nullable=False)

    else:
        id = ""
        input_text = ""
        source_lang = ""
        target_lang = ""
        translated_text = ""

    def __init__(self, *args, **kwargs):
        """initializes all translations"""
        super().__init__(*args, **kwargs)
