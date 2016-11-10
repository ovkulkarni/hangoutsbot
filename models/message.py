from ..database import BaseModel
from peewee import *

from .user import User
from .converstation import Conversation


class Message(BaseModel):
    conversation = ForeignKey(Conversation, related_name="messages")
    user = ForeignKey(User, related_name="messages")
    text = TextField()
    time = DateTimeField()
