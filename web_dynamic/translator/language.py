#!/usr/bin/python3
"""Get languages supported"""
import translator
from sqlalchemy import Column, String
from translator.translation_model import TranslationModel, Base
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class LanguageSupport(TranslationModel, Base):

    if translator.storage_type == "db":
        __tablename__ = 'languages_supported'
        id = Column(String(50), primary_key=True)
        code = Column(String(10), nullable=False)
        name = Column(String(50), nullable=False)


    else:
        code = ""
        name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
