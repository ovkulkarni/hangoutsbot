from ..database import BaseModel
from peewee import *
import sys
import importlib
import logging

logger = logging.getLogger(__name__)


class Command(BaseModel):
    name = CharField()
    admin_required = BooleanField()

    def run(self, user, args):
        if self.name not in sys.modules:
            logger.info("Importing formerly unimported command: {}".format(self.name))
            importlib.import_module("..commands.{}".format(self.name))
        sys.modules[self.name].Command.run(user, args)
