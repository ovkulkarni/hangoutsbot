from peewee import SqliteDatabase, Model

database = SqliteDatabase("hangoutsbot.db")


class BaseModel(Model):

    class Meta:
        database = database
