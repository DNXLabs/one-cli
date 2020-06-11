import glob
import importlib
import sys
from os.path import join
from os import path
from pathlib import Path

home = str(Path.home())


def load_plugins(source=home+'/.one/plugins/'):
    if path.exists(source):
        sys.path.append(home+'/.one')
        device_directories = glob.glob(join(source, "*.py"))
        if device_directories and path.exists(source + '__init__.py'):
            device_directories.remove(source + '__init__.py')
            for directory in device_directories:
                command_path = '.'.join(directory.rsplit('/', 2)[1:])[:-3]
                mod = importlib.import_module(command_path)
                __init__ = getattr(mod, '__init__')
                __init__()
