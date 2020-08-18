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
@click.option('-n', '--name', default=None, type=str, help='Workspace name.')
def change(name):
    workspaces = get_workspaces()

    if name == None:
        selected_workspace = workspace_question(workspaces)
    elif name in workspaces:
        selected_workspace = name
        click.echo('Selected workspace: ' + click.style(name, fg='red'))
    else:
        click.echo('Workspace not found.', err=True)
        selected_workspace = workspace_question(workspaces)

    f = open('.one.workspace', 'w')
    f.write('WORKSPACE=' + selected_workspace + '\n')
    f.close()

def workspace_question(workspaces):
    workspaces_obj = []
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
    selected_workspace = answers['workspace']
    
    return selected_workspace

