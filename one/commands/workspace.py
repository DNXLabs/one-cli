import click
import yaml
import os
from os import path, listdir
from one.utils.environment import home
from one.utils.prompt import style
from PyInquirer import prompt
from one.utils.workspace import get_workspaces


@click.group(help='Manage workspaces.')
def workspace():
    pass


#TODO Make fill yaml
# @workspace.command(help='Create and store workspace in a list.')
# def create():
# 	questions = [
# 		{
# 			'type': 'input',
# 			'name': 'AWS_ACCOUNT_ID',
# 			'message': 'What\'s your AWS_ACCOUNT_ID credential:',
# 			'validate': lambda text: len(text) >= 1 or 'Must be at least 1 characters.'
# 		},
# 		{
# 			'type': 'input',
# 			'name': 'AWS_ROLE',
# 			'message': 'What\'s your AWS_ROLE credential:',
# 			'validate': lambda text: len(text) >= 1 or 'Must be at least 1 characters.'
# 		},
# 		{
# 			'type': 'input',
# 			'name': 'WORKSPACE',
# 			'message': 'What\'s your WORKSPACE credential:',
# 			'validate': lambda text: len(text) >= 1 or 'Must be at least 1 characters.'
# 		}
# 	]

# 	answers = prompt(questions, style=style)


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

    f = open(home + '/.one/default', 'w')
    f.write('DEFAULT_WORKSPACE=' + answers['workspace'] + '\n')
    f.close()