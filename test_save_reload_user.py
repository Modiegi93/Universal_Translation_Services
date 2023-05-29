#!/usr/bin/python3
from translator import storage
from translator.translation_model import TranslationModel
from translator.user import User

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new User --")
my_user = User()
my_user.full_name = "Thapi Tee"
my_user.user_name = "Bar"
my_user.email = "universaltranslationlanguage@mail.com"
my_user.password = "root"
my_user.save()
print(my_user)

print("-- Create a new User 2 --")
my_user2 = User()
my_user2.full_name = "Chris Tee"
my_user2.user_name = "Kgosi"
my_user2.email = "universaltranslationlanguage1@mail.com"
my_user2.password = "root"
my_user2.save()
print(my_user2)
