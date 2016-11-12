from database import BaseModel
from peewee import *
import sys
import importlib
import logging
import asyncio
import settings

logger = logging.getLogger(__name__)


class Command(BaseModel):
    name = CharField()
    admin_required = BooleanField()

    @asyncio.coroutine
    def run(self, bot, conversation, user, args):
        if self.name not in sys.modules:
            logger.info("Importing formerly unimported command: {}".format(self.name))
            importlib.import_module("commands.{}".format(self.name))
        run = True
        if self.admin_required and not user.is_admin:
            run = False
        if run:
            yield from sys.modules[self.name].command.run(bot, conversation, user, args)
        else:
            yield from bot.send_message(conversation, "You're not an admin!")

    def __str__(self):
        return self.name


class BaseCommand(object):

    def __init__(self, name, config={}, parser=None, admin_required=False):
        self.name = name
        self.config = config
        self.parser = parser
        self.admin_required = admin_required

    @asyncio.coroutine
    def run(conversation, user, args):
        raise NotImplementedError("The `run` method must be implemented.")
