import click
from one.controller.workspace import WorkspaceController

workspace_controller = WorkspaceController()


@click.group(help='Manage workspaces.')
def workspace():
    pass


@workspace.command(name='list', help='List all workspaces.')
def _list():
    workspace_controller._list()


@workspace.command(help='Change environment variables to another workspace.')
def change():
    workspace_controller.change()
