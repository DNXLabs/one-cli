#!/usr/bin/env python3

import os, sys
from os import path
from pathlib import Path
import click
from one.docker.image import Image
from one.docker.container import Container
from one.utils.environment import Environment, home, load_environments
from one.__init__ import __version__, CLI_ROOT

if not path.exists(home + CLI_ROOT):
    os.mkdir(home + CLI_ROOT)

load_environments()


from one.commands.login import login
from one.commands.terraform import terraform
from one.commands.workspace import workspace
from one.commands.idp import idp
from one.commands.update import update


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


if __name__ == "__main__":
    cli()