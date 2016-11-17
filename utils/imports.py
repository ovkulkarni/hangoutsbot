import glob
import importlib
import settings
import os
import sys


def import_all(name, object_name):
    modules = glob.glob(os.path.join(settings.BASE_DIR, name) + "/*.py")
    all_objects = []
    for module in modules:
        module_name = os.path.basename(module)[:-3]
        if module_name == "__init__":
            continue
        importlib.import_module("{}.{}".format(name, module_name))
        all_objects.append(getattr(sys.modules["{}.{}".format(module_name)], object_name))
    return all_objects
