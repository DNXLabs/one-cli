from pathlib import Path

__version__ = '0.6.8'

home = str(Path.home())

CLI_ROOT = home + '/.one'
CONFIG_FILE = './one.yaml'
WORKSPACE_FILE = '.one/workspace'
