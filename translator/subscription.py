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


class Subscription(TranslationModel, Base):

    if translator.storage_type == "db":
        __tablename__ = "subscriptions"
        id = Column(String(50), primary_key=True)
        email = Column(String(100), nullable=False)
        plan = Column(String(100), nullable=False)
        amount = Column(String(100), nullable=False)

    else:
        id = ""
        email = ""
        plan = ""
        amount = ""

    def __init__(self, *args, **kwargs):
        """initializes all translations"""
        super().__init__(*args, **kwargs)
