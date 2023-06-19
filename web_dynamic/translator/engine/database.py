#!/usr/bin/python3
"""
Database Storage class
"""
import translator
from translator.text import TextTranslation
from translator.document import DocumentTranslation
from translator.image import ImageTranslation
from translator.website import WebsiteTranslation
from translator.detect_language import DetectLanguage
from translator.translation_model import TranslationModel, Base
from translator.language import LanguageSupport
from translator.feedback import FeedBack
from translator.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"TextTranslation": TextTranslation,
           "DocumentTranslation": DocumentTranslation,
           "ImageTranslation": ImageTranslation,
           "DetectLanguage": DetectLanguage, "FeedBack": FeedBack,
           "LanguageSupport": LanguageSupport, "User": User} 


class DataBase:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate the DataBase object"""
        ULT_MYSQL_USER = getenv('ULT_MYSQL_USER')
        ULT_MYSQL_PWD = getenv('ULT_MYSQL_PWD')
        ULT_MYSQL_HOST = getenv('ULT_MYSQL_HOST')
        ULT_MYSQL_DB = getenv('ULT_MYSQL_DB')
        ULT_ENV = getenv('ULT_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(ULT_MYSQL_USER,
                                             ULT_MYSQL_PWD,
                                             ULT_MYSQL_HOST,
                                             ULT_MYSQL_DB))
        
        if ULT_ENV == "test":
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sesh_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sesh_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """ method to retrieve one object """
        if (cls in classes or cls.__name__ in classes) and id is not None:
            if type(cls) != str:
                cls = classes[cls.__name__]
            else:
                cls = classes[cls]
            return self.__session.query(cls).filter(cls.id == id).first()
        else:
            return None

    def count(self, cls=None):
        """ a method to count the number of objects in storage """
        return len(self.all(cls))
