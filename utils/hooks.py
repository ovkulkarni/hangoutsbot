from models.hook import Hook

from hooks import all_hooks

import logging
import importlib

logger = logging.getLogger(__name__)


def register_hooks():
    # first we delete all the current registered hooks
    Hook.delete().execute()
    for hook in all_hooks:
        logger.debug("Creating {}".format(hook))
        Hook.create(name=hook.name, regex=hook.regex)
        importlib.import_module("hooks.{}".format(hook.name))
    return True
