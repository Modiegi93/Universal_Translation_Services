#!/usr/bin/python3
"""
Class WebsiteTranslation
"""
import json
import translator
import uuid
from translator.translation_model import TranslationModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Text


class WebsiteTranslation(TranslationModel, Base):

    if translator.storage_type == "db":
        __tablename__ = "website_translations"
        id = Column(String(60), primary_key=True)
        website_url = Column(String(4500), nullable=False)
        source_lang = Column(String(50), nullable=False)
        target_lang = Column(String(50), nullable=False)
        translated_html = Column(Text, nullable=False)

    else:
        id = ""
        website_url = ""
        source_lang = ""
        target_lang = ""
        translated_html = ""

    def __init__(self, *args, **kwargs):
        """initializes all translations"""
        super().__init__(*args, **kwargs)
