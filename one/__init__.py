# -*- coding: utf-8 -*-
import os

__version__ = os.getenv('CLI_VERSION', 'dev')

CLI_ROOT = '/.one'
CONFIG_FILE = './one.yaml'