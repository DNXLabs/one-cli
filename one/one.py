#!/usr/bin/env python3

import os
from os import path
import click
from one.__init__ import CLI_ROOT
from one.utils.environment.common import load_environments
from one.__init__ import __version__
from one.commands.app import app
from one.commands.idp import idp
from one.commands.init import init
from one.commands.auth import auth
from one.commands.update import update
from one.commands.terraform import terraform
from one.commands.workspace import workspace
from one.commands.aws import aws
from one.utils.plugins import load_plugins


if not path.exists(CLI_ROOT):
    os.mkdir(CLI_ROOT)

load_environments()


@click.version_option(__version__)
@click.group()
def cli():
    """CLI to manage all stacks from DNX."""
    pass


COMMAND_DIRS = [aws, app, idp, init, auth, update, terraform, workspace]


for command in COMMAND_DIRS:
    cli.add_command(command)

load_plugins()


if __name__ == "__main__":
    cli()
