#!/usr/bin/python3
import translator
from translator.translation_model import TranslationModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class FeedBack(TranslationModel, Base):
    """Representation of User feedback"""
    if translator.storage_type == "db":
        __tablename__ = "feedbacks"
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        text = Column(String(1024), nullable=False)

    else:
        user_id = ""
        text = ""

    def __repr__(self):
        """initializes feedback"""
        return f'<Feedback {self.id}>'
