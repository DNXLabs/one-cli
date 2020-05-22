import click
from one.utils.environment import home
from one.utils.prompt import style
from PyInquirer import prompt
from one.utils.workspace import get_workspaces
from one.__init__ import CLI_ROOT
from one.one import cli


def __init__():
    cli.add_command(workspace)

@click.group(help='Manage workspaces.')
def workspace():
    pass

@workspace.command(name='list', help='List all workspaces.')
def list_workspaces():
    workspaces = get_workspaces()
    for workspace in workspaces:
        print('- ' + workspace)

@workspace.command(help='Change environment variables to another workspace.')
def change():
    workspaces_obj = []
    workspaces = get_workspaces()
    for workspace in workspaces:
        workspaces_obj.append({'name': workspace})

    questions = [
        {
            'type': 'list',
            'message': 'Select workspace',
            'name': 'workspace',
            'choices': workspaces_obj
        }
    ]

    answers = prompt(questions, style=style)

    f = open(home + CLI_ROOT + '/default', 'w')
    f.write('DEFAULT_WORKSPACE=' + answers['workspace'] + '\n')
    f.close()
