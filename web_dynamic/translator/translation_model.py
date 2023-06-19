#!/usr/bin/python3
"""
Class Translation model
"""
from datetime import datetime
import translator
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import json

time = "%Y-%m-%dT%H:%M:%S.%f"

if translator.storage_type == "db":
    Base = declarative_base()
else:
    Base = object


class TranslationModel:
    """The TranslationModel class from which other classes will inherit from"""
    if translator.storage_type == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialization of the Translation model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the Translation class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        self.updated_at = datetime.utcnow()
        translator.storage.new(self)
        translator.storage.save()

    def to_dict(self):
        time = "%Y-%m-%dT%H:%M:%S.%f"
        new_dict = {}
        for key, value in self.__dict__.items():
            if key == "_sa_instance_state":
                continue
            if key == "created_at" or key == "updated_at":
                value = value.strftime(time)
            new_dict[key] = value
        new_dict["__class__"] = self.__class__.__name__
        return new_dict

        """def to_dict(self):
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_instance_translation" in new_dict:
            del new_dict["_instance_translation"]
        if "password" in new_dict and getenv("ULT_TYPE_STORAGE") == "db":
            del new_dict["password"]
        return new_dict"""

        """new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_instance_translation" in new_dict:
            del new_dict["_instance_translation"]
        if "password" in new_dict and getenv("ULT_TYPE_STORAGE") == "db":
            del new_dict["password"]
        return new_dict"""

    def delete(self):
        translator.storage.delete(self)


