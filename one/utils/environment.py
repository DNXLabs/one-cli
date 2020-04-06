import docker.utils
import os
from os import path
from pathlib import Path
from one.utils.workspace import get_workspace_value
from dotenv import load_dotenv


home = str(Path.home())


def get_env_idp():
    if path.exists(home + '/.one/idp'):
        env_idp = docker.utils.parse_env_file(home + '/.one/idp')
        return env_idp
    else:
        print('You do not have any idp configured, first setup your idp.')
        raise SystemExit


def load_environments():
    env_path_workspace = home + '/.one/default'
    load_dotenv(dotenv_path=env_path_workspace)


class Environment:

    def __init__(self):
        pass


    def build(self):
        envs = {}
        env_workspace = {}
        env_credentials = {}

        if path.exists(home + '/.one/credentials'):
            env_credentials = docker.utils.parse_env_file(home + '/.one/credentials')
        else:
            print('You are not logged in')
            raise SystemExit

        if os.getenv("DEFAULT_WORKSPACE"):
            workspace = os.getenv("DEFAULT_WORKSPACE")
            env_workspace = {}
            env_workspace['TF_VAR_aws_account_id'] = get_workspace_value(workspace, 'aws-account-id')
            env_workspace['TF_VAR_aws_role'] = get_workspace_value(workspace, 'aws-role')
            env_workspace['WORKSPACE'] = get_workspace_value(workspace, 'workspace')
        else:
            print('You do not have any workspace selected.')
            raise SystemExit

        envs = dict(env_credentials, **env_workspace)
        return envs