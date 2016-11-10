from ..database import BaseModel
from peewee import *
from playhouse import *

from .user import User
from .bot import Bot


class Conversation(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    members = ManyToManyField(User, related_name='conversations')
    name_locked = BooleanField()
    group = BooleanField()
