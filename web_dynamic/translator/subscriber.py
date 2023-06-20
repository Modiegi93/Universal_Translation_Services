#!/usr/bin/python3
"""
Class Subscriber
"""
import json
import uuid
import translator
from translator.translation_model import TranslationModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Text


class Subscriber(TranslationModel, Base):

    if translator.storage_type == "db":
        __tablename__ = "subscribers"
        id = Column(String(50), ForeignKey('user.id'),primary_key=True)
        email = Column(String(100), nullable=False)
        daily_newsletter = Column(String(100))

    else:
        id = ""
        email = ""
        daily_newsletter = ""

    def __init__(self, *args, **kwargs):
        """initializes all translations"""
        super().__init__(*args, **kwargs)
