#!/usr/bin/python3
"""Get languages supported"""
import translator
from sqlalchemy import Column, String
from translator.translation_model import TranslationModel, Base
import sqlalchemy
from sqlalchemy import Column, String

class LanguageSupport(TranslationModel, Base):

    if translator.storage_type == "db":
        __tablename__ = 'languages_supported'
        code = Column(String(10), primary_key=True)
        language = Column(String(50), nullable=False)

    else:
        code = ""
        language = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
