#!/usr/bin/python3
"""
Initialize the translator model
"""
from os import getenv

storage_type = getenv("ULT_TYPE_STORAGE")

if storage_type == "db":
    from translator.engine.database import DataBase
    storage = DataBase()

else:
    from translator.engine.filestorage import FileStorage
    storage = FileStorage()
storage.reload()
