import yaml
from os import path


def get_workspaces():
    workspaces = []
    if path.exists('./config.yaml'):
        with open('./config.yaml') as file:
            docs = yaml.load(file, Loader=yaml.FullLoader)
            for workspace in docs['workspaces']:
                for key in workspace.keys():
                    workspaces.append(key)
        file.close()
    else:
        print('No config file in current directory.')
        raise SystemExit

    return workspaces


def get_workspace_value(workspace, variable):
    if path.exists('./config.yaml'):
        with open('./config.yaml') as file:
            docs = yaml.load(file, Loader=yaml.FullLoader)
            for doc in docs['workspaces']:
                for key, value in doc.items():
                    if key == workspace:
                        return value[variable]
        file.close()
    else:
        print('No config file in current directory.')
        raise SystemExit
    return ''