#!/usr/bin/python3
"""
Class User
"""
import translator
from translator.translation_model import TranslationModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(TranslationModel, Base):
    """Representation of a user"""
    if translator.storage_type == "db":
        __tablename__ = 'users'
        username = Column(String(128), nullable=False)
        full_name = Column(String(128), nullable=True)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        feedback = relationship("FeedBack", backref="user")

    else:
        email = ""
        username = ""
        full_name = ""
        password = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """hash password"""
        if name == 'password':
            value = hashlib.md5(value.encode()).hexdigest()
        super.__setattr__(self, name, value)
