#!/usr/bin/python3
from datetime import datetime
import translator
from translator import storage
from translator.user import User

users = User(
    username="john_doe",
    full_name="John Doe",
    email="johndoe@example.com",
    password = "12345",
    created_at=datetime.now(),
    updated_at=datetime.now()
)

# Add the User object to the database
storage.new(users)
storage.save()

# Print the ID of the newly created User object
print("New User ID:", users.id)
