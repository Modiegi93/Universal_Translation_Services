#!/usr/bin/python3
from datetime import datetime
import translator
from translator import storage
from translator.feedback import FeedBack

feedbacks = FeedBack(
    user_id="user123",
    text="This translation service is amazing!",
    created_at=datetime.now(),
    updated_at=datetime.now()

)

# Add the FeedBack object to the database
storage.new(feedbacks)
storage.save()

# Print the ID of the newly created FeedBack object
print("New FeedBack ID:", feedbacks.id)
