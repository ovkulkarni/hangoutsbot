import glob
import importlib
import settings
import os
import sys

modules = glob.glob(os.path.join(settings.BASE_DIR, "commands") + "/*.py")

all_commands = []
for module in modules:
    module_name = os.path.basename(module)[:-3]
    if module_name == "__init__":
        continue
    importlib.import_module("commands.{}".format(module_name))
    all_commands.append(sys.modules["commands.{}".format(module_name)].command)
