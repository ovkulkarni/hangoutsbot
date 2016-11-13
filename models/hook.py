from database import BaseModel
from peewee import *

import sys
import importlib
import asyncio


class Hook(BaseModel):
    name = CharField()
    regex = CharField()

    @asyncio.coroutine
    def run(self, bot, conversation, user, text):
        if "hooks.{}".format(self.name) not in sys.modules:
            importlib.import_module("hooks.{}".format(self.name))
        yield from sys.modules["hooks.{}".format(self.name)].hook.run(bot, conversation, user, text)

    def __str__(self):
        return self.name
