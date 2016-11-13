from models.hook import Hook

from hooks import all_hooks

import logging
import sys
import importlib

logger = logging.getLogger(__name__)


def register_hooks():
    # first we delete all the current registered hooks
    Hook.delete().execute()
    for hook in all_hooks:
        logger.debug("Creating {}".format(hook))
        if "hooks.{}".format(hook.name) in sys.modules:
            Hook.delete().execute()
            raise NameError("Multiple hooks with same name found! Cleaning up and exiting...")
        Hook.create(name=hook.name, regex=hook.regex)
        importlib.import_module("hooks.{}".format(hook.name))
    return True
