import click
import docker.utils
from pathlib import Path
from dotenv import load_dotenv
from os import path
from one.__init__ import CLI_ROOT


home = str(Path.home())


def get_env_idp():
    if path.exists(get_cli_root() + '/idp'):
        env_idp = docker.utils.parse_env_file(get_cli_root() + '/idp')
        return env_idp
    else:
        click.echo('You do not have any idp configured, first setup your idp.')
        raise SystemExit


def load_environments():
    env_path_workspace = '.one.workspace'
    load_dotenv(dotenv_path=env_path_workspace)


def get_cli_root():
    return home + CLI_ROOT
