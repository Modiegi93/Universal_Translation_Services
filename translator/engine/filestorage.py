#!/usr/bin/python3
"""
Filestorage Storage class
"""
import os
import json
import translator
from translator.translation_model import TranslationModel
from translator.text import TextTranslation
from translator.document import DocumentTranslation
from translator.image import ImageTranslation
from translator.website import WebsiteTranslation
from translator.detect_language import DetectLanguage
from translator.language import LanguageSupport
from translator.feedback import FeedBack
from translator.subscription import Subscription
from translator.user import User

classes = {"TranslationModel": TranslationModel,
           "TextTranslation": TextTranslation,
           "DocumentTranslation": DocumentTranslation,
           "ImageTranslation": ImageTranslation,
           "DetectLanguage": DetectLanguage, "FeedBack": FeedBack,
           "Subscription": Subscription,
           "LanguageSupport": LanguageSupport, "User": User}


class FileStorage:
    """Serializes instances to a JSON file and deserializes
    back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """ A method to retrieve one object """
        clss = self.all(cls)
        if type(cls) != str:
            cls = cls.__name__
        key = cls + '.' + id
        return clss.get(key)

    def count(self, cls=None):
        """ A method to count the number of objects in storage """
        return len(self.all(cls))
