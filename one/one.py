#!/usr/bin/env python3

import os
from os import path
import click
from one.utils.environment.common import load_environments, get_cli_root
from one.__init__ import __version__
from one.commands.app import app
from one.commands.idp import idp
from one.commands.init import init
from one.commands.login import login
from one.commands.terraform import terraform
from one.commands.workspace import workspace
from one.utils.load_plugins import load_plugins


if not path.exists(get_cli_root()):
    os.mkdir(get_cli_root())

load_environments()


@click.version_option(__version__)
@click.group()
def cli():
    """CLI to manage all stacks from DNX."""
    pass


COMMAND_DIRS = [app, idp, init, login, terraform, workspace]


for command in COMMAND_DIRS:
    cli.add_command(command)

load_plugins()


if __name__ == "__main__":
    cli()
