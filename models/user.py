from ..database import BaseModel
from peewee import *


class User(BaseModel):
    id = IntegerField(primary_key=True)
    first_name = CharField()
    last_name = CharField()
    is_admin = BooleanField()

    @property
    def username(self):
        return "{}{}".format(self.first_name[0].lower(), self.last_name.lower())

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)
