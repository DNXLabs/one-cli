import click
from one.utils.environment.idp import config_idp


@click.group(help='Manage the IDP configuration in your local.')
def idp():
    pass


@idp.command(help='Configure IDP to be used.')
def config():
    config_idp()
