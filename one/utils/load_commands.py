import glob
import sys
import os
import pathlib
import importlib

COMMAND_DIRS = ['idp', 'init', 'login', 'terraform', 'update', 'workspace']

def load_commands(source='one/commands'):
    for command in COMMAND_DIRS:
        command_path = 'one.commands.' + command
        mod = importlib.import_module(command_path)
        __init__ = getattr(mod, '__init__')
        __init__()
