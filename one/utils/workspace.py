import yaml
from os import path
from one.__init__ import CONFIG_FILE

def get_workspaces():
    workspaces = []
    if not path.exists(CONFIG_FILE):
        print('No config file in current directory.')
        raise SystemExit

    with open(CONFIG_FILE) as file:
        docs = yaml.load(file, Loader=yaml.FullLoader)
        for workspace_key in docs['workspaces'].keys():
            workspaces.append(workspace_key)
    file.close()

    return workspaces


def get_workspace_value(workspace_name, variable, default=None):
    if not path.exists(CONFIG_FILE):
        print('No config file in current directory.')
        raise SystemExit

    with open(CONFIG_FILE) as file:
        docs = yaml.load(file, Loader=yaml.FullLoader)
        if workspace_name not in docs['workspaces']:
            print('Workspace %s not found', workspace_name)
            raise SystemExit

        workspace = docs['workspaces'][workspace_name]

        if variable in workspace:
            value = workspace[variable]
        elif default == None:
            print('Missing required parameter in config: workspaces.%s.%s' % (workspace_name,variable))
            raise SystemExit
        else:
            value = default
    file.close()

    return str(value)