import glob
import importlib
import settings
import os
import sys

modules = glob.glob(os.path.join(settings.BASE_DIR, "hooks") + "/*.py")

all_hooks = []
for module in modules:
    module_name = os.path.basename(module)[:-3]
    if module_name == "__init__":
        continue
    importlib.import_module("hooks.{}".format(module_name))
    all_hooks.append(sys.modules["hooks.{}".format(module_name)].hook)
