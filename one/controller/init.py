import yaml
from PyInquirer import prompt
from one.__init__ import CONFIG_FILE
from one.prompt.init import CREATION_QUESTION, IMAGE_QUESTIONS, WORKSPACE_QUESTIONS
from one.utils.prompt import style


class InitController():

    workspaces = {}
    images = {}
    create_workspace = 'y'

    def __init__(self):
        pass

    def init(self):
        try:
            self.prompt_create_workspace_questions()

            if self.create_workspace == 'y':
                self.prompt_image_questions()
                self.prompt_credential_questions()
                self.write_config()
        except KeyError:
            raise SystemExit

    def prompt_create_workspace_questions(self):
        answer = prompt(CREATION_QUESTION, style=style)
        self.create_workspace = answer['create'].lower()

    def prompt_image_questions(self):
        image_answers = prompt(IMAGE_QUESTIONS, style=style)
        self.images = {
            'terraform': image_answers['terraform'],
            'azure': image_answers['azure'],
            'gsuite': image_answers['gsuite']
        }

    def prompt_credential_questions(self):
        while True:
            workspace_answers = prompt(WORKSPACE_QUESTIONS, style=style)
            if workspace_answers['assume_role'].lower() == 'y':
                assume_role = True
            else:
                assume_role = False
            workspace = {
                'aws-role': workspace_answers['AWS_ROLE'],
                'aws-account-id': workspace_answers['AWS_ACCOUNT_ID'],
                'assume-role': assume_role
            }
            self.workspaces[workspace_answers['WORKSPACE']] = workspace
            if workspace_answers['new_workspace'].lower() == 'n':
                break

    def write_config(self):
        with open(CONFIG_FILE, 'w') as file:
            content = {'images': self.images, 'workspaces': self.workspaces}
            yaml.dump(content, file)
