import click
from one.utils.prompt import style
from PyInquirer import prompt
from one.utils.config import get_workspaces


@click.group(help='Manage workspaces.')
def workspace():
    pass


@workspace.command(name='list', help='List all workspaces.')
def list_workspaces():
    workspaces = get_workspaces()
    for workspace in workspaces:
        click.echo('- ' + workspace)


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

    f = open('.one.workspace', 'w')
    f.write('WORKSPACE=' + answers['workspace'] + '\n')
    f.close()
