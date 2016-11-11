from peewee import SqliteDatabase, Model

import settings

database = SqliteDatabase(settings.DATABASE_PATH)


class BaseModel(Model):

    class Meta:
        database = database
