import yaml
import click
from PyInquirer import prompt
from os import path
from one.__init__ import CONFIG_FILE, DEFAULT_WORKSPACE
from one.utils.prompt import style


class WorkspaceController():

    workspaces = []

    def __init__(self):
        pass

    def _list(self):
        self.get_workspaces()
        for workspace in self.workspaces:
            click.echo('- ' + workspace)

    def prompt_workspaces_list(self, workspaces_obj):
        questions = [
            {
                'type': 'list',
                'message': 'Select workspace',
                'name': 'workspace',
                'choices': workspaces_obj
            }
        ]

        answers = prompt(questions, style=style)
        return answers['workspace']

    def change(self):
        workspaces_obj = self.format_workspace_list()
        if workspaces_obj:
            try:
                selected_workspace = self.prompt_workspaces_list(workspaces_obj)
                content = 'WORKSPACE=%s\n' % (selected_workspace)
                self.write_default_workspace(content)
            except IndexError:
                raise SystemExit

    def get_workspaces(self):
        if path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as file:
                docs = yaml.load(file, Loader=yaml.BaseLoader)
                for workspace_key in docs['workspaces'].keys():
                    self.workspaces.append(workspace_key)
            file.close()

        return self.workspaces

    def format_workspace_list(self):
        workspaces_obj = []
        self.get_workspaces()
        for workspace in self.workspaces:
            workspaces_obj.append({'name': workspace})
        return workspaces_obj

    def write_default_workspace(self, content):
        with open(DEFAULT_WORKSPACE, 'w') as file:
            file.write(content)
