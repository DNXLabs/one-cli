import yaml
from os import path

def get_workspaces():
    workspaces = []
    if path.exists('./one.yaml'):
        with open('./one.yaml') as file:
            docs = yaml.load(file, Loader=yaml.FullLoader)
            for workspace_key in docs['workspaces'].keys():
                workspaces.append(workspace_key)
        file.close()
    else:
        print('No config file in current directory.')
        raise SystemExit

    return workspaces


def get_workspace_value(workspace, variable):
    if path.exists('./one.yaml'):
        with open('./one.yaml') as file:
            docs = yaml.load(file, Loader=yaml.FullLoader)
            for workspace_key in docs['workspaces'].keys():
                if workspace_key == workspace:
                    return docs['workspaces'][workspace_key]
        file.close()
    else:
        print('No config file in current directory.')
        raise SystemExit
    return ''