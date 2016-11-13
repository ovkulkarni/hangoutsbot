from database import BaseModel
from peewee import CharField, BooleanField


class User(BaseModel):
    id = CharField(primary_key=True)
    first_name = CharField()
    last_name = CharField()
    is_admin = BooleanField(default=False)

    @property
    def username(self):
        return "{}{}".format(self.first_name.lower(), self.last_name.lower()).replace(" ", "")

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.full_name
