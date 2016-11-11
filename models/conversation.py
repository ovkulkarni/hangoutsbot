from database import BaseModel
from peewee import *
from playhouse.fields import *

from .user import User


class Conversation(BaseModel):
    id = CharField(primary_key=True)
    members = ManyToManyField(User, related_name='conversations')
    group = BooleanField()

    def __str__(self):
        return self.id
