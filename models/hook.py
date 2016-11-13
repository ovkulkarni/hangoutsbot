from database import BaseModel
from peewee import *


class Hook(BaseModel):
    name = CharField()
    regex = CharField()
