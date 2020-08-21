import glob
import importlib
import sys
from os.path import join
from os import path
from pathlib import Path

home = str(Path.home())

def load_plugins(source=home+'/.one/plugins/'):
    if path.exists(source):
        sys.path.append(source)
        for directory in glob.glob(join(source, "*/")):
            if path.exists(directory + '__init__.py'):
                plugin_name = directory.rsplit('/')[-2]
                getattr(importlib.import_module(plugin_name), '__init__')()