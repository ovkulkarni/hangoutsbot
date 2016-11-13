from database import BaseModel
from peewee import CharField, BooleanField
from playhouse.fields import ManyToManyField

from .user import User

import settings

import logging
import logging.handlers
import os


class Conversation(BaseModel):
    id = CharField(primary_key=True)
    members = ManyToManyField(User, related_name='conversations')
    group = BooleanField()

    @property
    def logger(self):
        message_logger = logging.getLogger(self.id)
        message_formatter = logging.Formatter('[%(message_time)s] <%(username)s> %(message)s')
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(settings.LOGGING_DIRECTORY, '{}.log'.format(self.id)), maxBytes=20000000, backupCount=5)
        file_handler.setFormatter(message_formatter)
        message_logger.setLevel(logging.INFO)
        if len(message_logger.handlers) > 0:
            for handler in message_logger.handlers:
                if not isinstance(handler, logging.handlers.RotatingFileHandler):
                    message_logger.addHandler(file_handler)
        else:
            message_logger.addHandler(file_handler)
        return message_logger

    def __str__(self):
        return self.id
