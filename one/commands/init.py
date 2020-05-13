import click
from PyInquirer import prompt
import yaml
from one.utils.prompt import style
from one.docker.image import AZURE_AUTH_IMAGE, GSUITE_AUTH_IMAGE, TERRAFORM_IMAGE
from one.__init__ import CONFIG_FILE

creation_question =  [
    {
        'type': 'input',
        'name': 'create',
        'message': 'Do you want to create workspaces now? [Y/n]',
        'default': 'Y'
    }
]

image_questions = [
    {
        'type': 'input',
        'name': 'terraform',
        'default': TERRAFORM_IMAGE,
        'message': 'Terraform docker image:',
        'validate': lambda text: len(text) >= 4 or 'Must be at least 4 character.'
    },
    {
        'type': 'input',
        'name': 'gsuite',
        'default': GSUITE_AUTH_IMAGE,
        'message': 'G Suite docker image:',
        'validate': lambda text: len(text) >= 4 or 'Must be at least 4 character.'
    },
    {
        'type': 'input',
        'name': 'azure',
        'default': AZURE_AUTH_IMAGE,
        'message': 'Azure docker image:',
        'validate': lambda text: len(text) >= 4 or 'Must be at least 4 character.'
    },
]

workspace_questions = [
    {
        'type': 'input',
        'name': 'AWS_ACCOUNT_ID',
        'message': 'What\'s your AWS_ACCOUNT_ID credential:',
        'validate': lambda text: len(text) >= 1 or 'Must be at least 1 character.'
    },
    {
        'type': 'input',
        'name': 'AWS_ROLE',
        'message': 'What\'s your AWS_ROLE credential:',
        'validate': lambda text: len(text) >= 1 or 'Must be at least 1 character.'
    },
    {
        'type': 'input',
        'name': 'WORKSPACE',
        'message': 'What\'s your WORKSPACE credential:',
        'validate': lambda text: len(text) >= 1 or 'Must be at least 1 character.'
    },
    {
        'type': 'input',
        'name': 'assume_role',
        'default': 'n',
        'message': 'Do you want to this workspace to assume role? [Y/n]'
    },
    {
        'type': 'input',
        'name': 'new_workspace',
        'default': 'Y',
        'message': 'Do you want to create another workspace? [Y/n]'
    }
]

@click.command(help='Create config file for CLI in current directory.')
def init():
    create_answer = prompt(creation_question, style=style)
    create_workspace = create_answer['create'].lower()
    workspaces = {}
    if create_workspace == 'y' or not create_workspace:
        image_answers = prompt(image_questions, style=style)
        images = {
            'terraform': image_answers['terraform'],
            'gsuite': image_answers['gsuite'],
            'azure': image_answers['azure']
        }

        while True:
            workspace_answers = prompt(workspace_questions, style=style)
            if workspace_answers['assume_role'].lower() == 'y' or not workspace_answers['assume_role']:
                assume_role = True
            else:
                assume_role = False
            workspace = {
                            'aws-role': workspace_answers['AWS_ROLE'],
                            'aws-account-id': workspace_answers['AWS_ACCOUNT_ID'],
                            'assume-role': assume_role
                        }
            workspaces[workspace_answers['WORKSPACE']] = workspace
            if workspace_answers['new_workspace'].lower() == 'n':
                break
        with open(CONFIG_FILE, 'w') as file:
            content = {'images': images, 'workspaces': workspaces}
            yaml.dump(content, file)