import glob
import importlib
import sys
from os.path import join
from pathlib import Path

home = str(Path.home())


def load_plugins(source=home+'/.one/plugins/'):
    sys.path.append(home+'/.one')
    device_directories = glob.glob(join(source, "*.py"))
    device_directories.remove(source + '__init__.py')
    for directory in device_directories:
        command_path = directory.strip('./')[:-3].replace('/', '.').split('.', 4)[-1]
        mod = importlib.import_module(command_path)
        __init__ = getattr(mod, '__init__')
        __init__()
