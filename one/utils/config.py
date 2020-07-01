import click
import yaml
from os import path
from one.__init__ import CONFIG_FILE


if not path.exists('./one.yaml'):
    click.echo(
        click.style('WARN ', fg='yellow') +
        'No config file in current directory.\n'
    )


def get_config_value(key, default=None):
    value = default
    if path.exists(CONFIG_FILE):
        with open('./one.yaml') as file:
            docs = yaml.load(file, Loader=yaml.BaseLoader)
            for key_path in key.split('.'):
                if key_path not in docs:
                    break
                if isinstance(docs[key_path], str):
                    value = docs[key_path]
                docs = docs[key_path]

        if value is None:
            click.echo('Required parameter: %s' % key)
            raise SystemExit

    return value


def get_workspaces():
    workspaces = []
    if path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as file:
            docs = yaml.load(file, Loader=yaml.BaseLoader)
            for workspace_key in docs['workspaces'].keys():
                workspaces.append(workspace_key)
        file.close()

    return workspaces


def get_workspace_value(workspace_name, variable, default=None):
    value = default
    if path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as file:
            docs = yaml.load(file, Loader=yaml.BaseLoader)
            if workspace_name not in docs['workspaces']:
                if workspace_name is None:
                    click.echo('Please set workspace before continuing')
                else:
                    click.echo('Workspace %s not found' % (workspace_name))
                raise SystemExit

            workspace = docs['workspaces'][workspace_name]

            if variable in workspace:
                value = workspace[variable]
            elif default is None:
                click.echo('Missing required parameter in config: workspaces.%s.%s' % (workspace_name, variable))
                raise SystemExit
            else:
                value = default
        file.close()

    return str(value)
