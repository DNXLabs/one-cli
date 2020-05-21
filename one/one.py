#!/usr/bin/env python3

import os
from os import path
import click
from one.utils.environment import home, load_environments
from one.__init__ import __version__, CLI_ROOT
from one.commands.login import login
from one.commands.terraform import terraform
from one.commands.workspace import workspace
from one.commands.idp import idp
from one.commands.update import update
from one.commands.init import init


if not path.exists(home + CLI_ROOT):
    os.mkdir(home + CLI_ROOT)

load_environments()


@click.version_option(__version__)
@click.group()
def cli():
    """CLI to manage all stacks from DNX."""
    pass


cli.add_command(login)
cli.add_command(terraform)
cli.add_command(workspace)
cli.add_command(idp)
cli.add_command(update)
cli.add_command(init)


if __name__ == "__main__":
    cli()
