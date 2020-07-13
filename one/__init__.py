from pathlib import Path

__version__ = '0.5.1'

home = str(Path.home())

CLI_ROOT = home + '/.one'
CONFIG_FILE = './one.yaml'
DEFAULT_WORKSPACE = '.one.workspace'
