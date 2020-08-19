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
@click.option('-w', '--workspace', default=None, type=str, help='Workspace name.')
def change(workspace: str):
    workspaces = get_workspaces()

    if workspace in workspaces:
        click.echo('Selected workspace: ' + click.style(workspace, fg='green', bold=True))
    else:
        if workspace:
            click.echo('Workspace ' + click.style(workspace, fg='red', bold=True) + ' not found.', err=True)

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
        try:
            answers = prompt(questions, style=style)
        except KeyError:
            raise SystemExit
        workspace = answers.get('workspace', 'default')

    f = open('.one.workspace', 'w')
    f.write('WORKSPACE=' + workspace + '\n')
    f.close()
