from database import BaseModel
from peewee import ForeignKeyField, TextField, DateTimeField

from .user import User
from .conversation import Conversation


class Message(BaseModel):
    conversation = ForeignKeyField(Conversation, related_name="messages")
    user = ForeignKeyField(User, related_name="messages")
    text = TextField()
    time = DateTimeField()

    def __str__(self):
        return "{} - {}".format(self.user, self.text)
