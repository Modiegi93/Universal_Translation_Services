#!/usr/bin/python3
"""
Class DetectLanguage
"""
import json
import uuid
import translator
from translator.translation_model import TranslationModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Text


class DetectLanguage(TranslationModel, Base):

    if translator.storage_type == "db":
        __tablename__ = "detect_languages"
        id = Column(String(60), primary_key=True)
        input_text = Column(String(4500), nullable=False)
        detected_lang = Column(String(50), nullable=False)
        

    else:
        id = ""
        input_text = ""
        detected_lang = ""

    def __init__(self, *args, **kwargs):
        """initializes all translations"""
        super().__init__(*args, **kwargs)
