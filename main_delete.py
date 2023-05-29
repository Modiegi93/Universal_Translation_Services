#!/usr/bin/python3
""" Test delete feature
"""
from translator.engine.filestorage import FileStorage
from translator.text import TextTranslation

fs = FileStorage()

# All TextTranslations
all_texts = fs.all(TextTranslation)
print("All text_translations: {}".format(len(all_texts.keys())))
for text_key in all_texts.keys():
    print(all_texts[text_key])

# Create a new translation
new_text = TextTranslation()
new_text.name = "Hello, how are you?"
fs.new(new_text)
fs.save()
print("New Text: {}".format(new_text))

# All States
all_texts = fs.all(TextTranslation)
print("All Texts: {}".format(len(all_texts.keys())))
for text_key in all_texts.keys():
    print(all_texts[text_key])

# Create another State
another_text = TextTranslation()
another_text.name = "I love you!"
fs.new(another_text)
fs.save()
print("Another Text: {}".format(another_text))

# All States
all_texts= fs.all(TextTranslation)
print("All Texts: {}".format(len(all_texts.keys())))
for text_key in all_texts.keys():
    print(all_texts[text_key])        

# Delete the new State
fs.delete(new_text)

# All States
all_texts = fs.all(TextTranslation)
print("All Texts: {}".format(len(all_texts.keys())))
for text_key in all_texts.keys():
    print(all_texts[text_key])

