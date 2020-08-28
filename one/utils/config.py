import click
import os
import yaml
import re
from packaging.version import parse
from os import path
from one.__init__ import CONFIG_FILE, __version__
from one.utils.operators import OPERATORS


if not path.exists(CONFIG_FILE):
    click.echo(
        click.style('WARN ', fg='yellow') +
        'No config file in current directory.\n'
    )


def required_version_check():
    versions = get_config_value('required_version', '')
    if versions:
        required_versions = re.split(r'[,]\s*', versions)
        for version in required_versions:
            try:
                operator = OPERATORS[version.split(' ', 1)[0]]
                required_version = parse(version.split(' ')[1])
                if not operator(parse(__version__), required_version):
                    click.echo(
                        click.style('ERROR ', fg='red') +
                        'Config file requires one-cli version %s and your current version is %s.\n' % (version, __version__))
                    raise SystemExit
            except KeyError:
                click.echo(
                    click.style('ERROR ', fg='red') +
                    'Wrong configuration for required_version in one.yaml.\n')
                raise SystemExit


def get_config_value(key, default=None):
    value = default
    if path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as file:
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


def get_workspace_value(workspace_name, variable, default=None):
    value = default
    if path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as file:
            docs = yaml.load(file, Loader=yaml.BaseLoader)
            if workspace_name not in docs['workspaces']:
                if workspace_name is None:
                    click.echo('Please set workspace before continuing.')
                else:
                    click.echo('Workspace %s not found.' % (workspace_name))
                raise SystemExit

            layer = docs['workspaces'][workspace_name]
            keys = variable.split('.')

            for key_path in keys:
                if key_path in layer:
                    if key_path == keys[-1]:  # Last key
                        value = layer[key_path]
                    else:
                        layer = layer[key_path]
                else:
                    break

            if not value:
                click.echo('Missing required parameter in config: workspaces.%s.%s.' % (workspace_name, variable))
                raise SystemExit

        file.close()

    return str(value)


def get_current_workspace_value(default=None):
    return os.getenv('WORKSPACE') or 'default'


def get_workspaces():
    workspaces = []
    if path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as file:
            docs = yaml.load(file, Loader=yaml.BaseLoader)
            for workspace_key in docs['workspaces'].keys():
                workspaces.append(workspace_key)
        file.close()

    return workspaces
