#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from translator import storage
from translator.text import TextTranslation

print("All objects: {}".format(storage.count()))
print("Text objects: {}".format(storage.count(TextTranslation)))

first_text_id = list(storage.all(TextTranslation).values())[0].id
print("First text: {}".format(storage.get(TextTranslation, first_text_id)))
