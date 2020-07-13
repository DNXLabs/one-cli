import click
from one.controller.init import InitController


@click.command(help='Create config file for CLI in current directory.')
def init():
    InitController().init()
