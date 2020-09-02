import click
from PyInquirer import prompt
import yaml
from one.utils.prompt import style
from one.__init__ import CONFIG_FILE
from one.prompt.init import CREATION_QUESTION, IMAGE_QUESTIONS, WORKSPACE_QUESTIONS


@click.command(help='Create config file for CLI in current directory.')
def init():
    create_answer = prompt(CREATION_QUESTION, style=style)
    create_workspace = create_answer['create'].lower()
    workspaces = {}
    if create_workspace == 'y' or not create_workspace:
        image_answers = prompt(IMAGE_QUESTIONS, style=style)
        images = {
            'terraform': image_answers['terraform'],
            'gsuite': image_answers['gsuite'],
            'azure': image_answers['azure']
        }

        while True:
            workspace_answers = prompt(WORKSPACE_QUESTIONS, style=style)
            if workspace_answers['assume_role'].lower() == 'y' or not workspace_answers['assume_role']:
                assume_role = True
            else:
                assume_role = False
            workspace = {
                'aws': {
                    'role': workspace_answers['AWS_ROLE'],
                    'account_id': workspace_answers['AWS_ACCOUNT_ID'],
                    'assume_role': assume_role
                }
            }
            workspaces[workspace_answers['WORKSPACE']] = workspace
            if workspace_answers['new_workspace'].lower() == 'n':
                break
        with open(CONFIG_FILE, 'w') as file:
            content = {'images': images, 'workspaces': workspaces}
            yaml.dump(content, file)
