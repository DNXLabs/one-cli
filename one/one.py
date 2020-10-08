#!/usr/bin/env python3

import os
from os import path
import click
from dotenv import load_dotenv
from one.__init__ import __version__, WORKSPACE_FILE, CLI_ROOT
from one.commands.app import app
from one.commands.init import init
from one.commands.auth import auth
from one.commands.terraform import terraform
from one.commands.workspace import workspace
from one.commands.aws import aws, aws_v2
from one.commands.shell import shell
from one.utils.plugins import load_plugins
from one.utils.config import required_version_check


if not path.exists(CLI_ROOT):
    os.mkdir(CLI_ROOT)

required_version_check()

load_dotenv(dotenv_path=WORKSPACE_FILE)


@click.version_option(__version__)
@click.group()
def cli():
    """CLI to manage all stacks from DNX."""
    pass


COMMAND_DIRS = [aws, aws_v2, shell, app, init, auth, terraform, workspace]


for command in COMMAND_DIRS:
    cli.add_command(command)

load_plugins()


if __name__ == "__main__":
    cli()
