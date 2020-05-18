import docker.utils
import os
from os import path
from pathlib import Path
from one.utils.workspace import get_workspace_value
from one.utils.parse_env import parse_env
from dotenv import load_dotenv
from one.docker.container import Container
from one.docker.image import Image
from one.__init__ import CLI_ROOT


home = str(Path.home())


def get_env_idp():
    if path.exists(home + CLI_ROOT + '/idp'):
        env_idp = docker.utils.parse_env_file(home + CLI_ROOT + '/idp')
        return env_idp
    else:
        print('You do not have any idp configured, first setup your idp.')
        raise SystemExit


def load_environments():
    env_path_workspace = home + CLI_ROOT + '/default'
    load_dotenv(dotenv_path=env_path_workspace)


class Environment:

    def __init__(self):
        pass


    def build(self):
        envs = {}
        env_workspace = {}
        env_credentials = {}

        if path.exists(home + CLI_ROOT + '/credentials'):
            env_credentials = docker.utils.parse_env_file(home + CLI_ROOT + '/credentials')
        else:
            print('Please login before proceeding')
            raise SystemExit

        if not os.getenv("DEFAULT_WORKSPACE"):
            print('Please select a workspace before proceeding')
            raise SystemExit

        workspace = os.getenv("DEFAULT_WORKSPACE")
        env_aws_account_id = get_workspace_value(workspace, 'aws-account-id')
        env_aws_role = get_workspace_value(workspace, 'aws-role')
        aws_assume_role = get_workspace_value(workspace, 'aws-assume-role', 'false')

        env_workspace = {}
        env_workspace['TF_VAR_aws_account_id'] = env_aws_account_id
        env_workspace['TF_VAR_aws_role'] = env_aws_role
        env_workspace['WORKSPACE'] = workspace

        if aws_assume_role.lower() == "true":
            assume_creds = self.aws_assume_role(credentials=env_credentials, role=env_aws_role, account_id=env_aws_account_id)
            env_credentials.update(assume_creds)

        envs = dict(env_credentials, **env_workspace)
        return envs

    def aws_assume_role(self, credentials, role, account_id):
        container = Container()
        image = Image()

        AWS_IMAGE = image.get_image('aws')
        envs = {
            "AWS_ROLE": role,
            "AWS_ACCOUNT_ID": account_id,
        }
        envs.update(credentials)

        command = 'assume-role.sh'
        output = container.create(
            image=AWS_IMAGE,
            entrypoint='/bin/bash -c',
            command=command,
            volume='/work',
            environment=envs,
            tty=False, stdin_open=False)

        return parse_env("\n".join(output.decode("utf-8").splitlines()))
