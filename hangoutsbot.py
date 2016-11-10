#!/usr/bin/env python3

import logging
import asyncio
import os
import sys
import hangups
import yaml

import settings

from models.user import User
from models.conversation import Conversation
from models.message import Message

from utils.commands import register_commands

logger = logging.getLogger(__name__)

logger.basicConfig(format="%(levelname)s: %(asctime)s %(message)s")


class HangoutsBot(object):

    def __init__(self):
        with open(settings.CONFIG_FILE, "r") as f:
            self.config = yaml.load(f.read())
        register_commands()
        self.client = None
