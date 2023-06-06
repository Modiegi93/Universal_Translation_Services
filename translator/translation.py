#!/usr/bin/python3
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Create the SQLAlchemy engine and session
engine = create_engine('sqlite:///translations.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Translation(Base):
    __tablename__ = 'translations'
    id = Column(Integer, primary_key=True)
    source_text = Column(String)
    translated_text = Column(String)
    source_lang = Column(String)
    target_lang = Column(String)
    timestamp = Column(DateTime)

    def __init__(self, source_text, translated_text, source_lang, target_lang, timestamp):
        self.source_text = source_text
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.timestamp = timestamp

# Update the TranslationServices class
class TranslationServices:
    def __init__(self):
        self.history = []

    def add_translation(self, source_text, translated_text, source_lang,
                        target_lang, timestamp):
        translation = Translation(source_text, translated_text, source_lang,
                                  target_lang, timestamp)
        self.history.append(translation)
        session.add(translation)
        session.commit()

    def get_translation_history(self):
        return self.history

# Create the translations table in the database
Base.metadata.create_all(engine)
