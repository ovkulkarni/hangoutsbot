from models.command import Command

from commands import all_commands

import logging
import importlib

logger = logging.getLogger(__name__)


def register_commands():
    # first we delete all the current registered commands
    Command.delete().execute()
    for command in all_commands:
        logger.debug("Creating {}".format(command))
        Command.create(name=command.name, admin_required=command.admin_required)
        importlib.import_module("commands.{}".format(command.name))
    return True
