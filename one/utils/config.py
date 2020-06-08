import yaml
from os import path
from one.__init__ import CONFIG_FILE


def get_config_value(key, default=None):
    if not path.exists('./one.yaml'):
        print('No config file in current directory.')
        raise SystemExit

    value = default

    with open('./one.yaml') as file:
        docs = yaml.load(file, Loader=yaml.BaseLoader)
        for key_path in key.split('.'):
            if not key_path in docs:
                break
            if isinstance(docs[key_path], str):
                value = docs[key_path]
            docs = docs[key_path]

    if value == None:
        print('Required parameter: %s' % key)
        raise SystemExit

    return value

def get_workspaces():
    workspaces = []
    if not path.exists(CONFIG_FILE):
        print('No config file in current directory.')
        raise SystemExit

    with open(CONFIG_FILE) as file:
        docs = yaml.load(file, Loader=yaml.BaseLoader)
        for workspace_key in docs['workspaces'].keys():
            workspaces.append(workspace_key)
    file.close()

    return workspaces


def get_workspace_value(workspace_name, variable, default=None):
    if not path.exists(CONFIG_FILE):
        print('No config file in current directory.')
        raise SystemExit

    with open(CONFIG_FILE) as file:
        docs = yaml.load(file, Loader=yaml.BaseLoader)
        if workspace_name not in docs['workspaces']:
            print('Workspace %s not found' % (workspace_name))
            raise SystemExit

        workspace = docs['workspaces'][workspace_name]

        if variable in workspace:
            value = workspace[variable]
        elif default is None:
            print('Missing required parameter in config: workspaces.%s.%s' % (workspace_name, variable))
            raise SystemExit
        else:
            value = default
    file.close()

    return str(value)
