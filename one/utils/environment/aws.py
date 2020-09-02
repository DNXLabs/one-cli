import click
import docker.utils
from os import path, getenv
from one.utils.config import get_workspace_value
from one.utils.parse_env import parse_env
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment import Environment
from one.__init__ import CLI_ROOT


class EnvironmentAws(Environment):
    def __init__(self):
        super().__init__()
        self.env_auth = {}
        self.env_assume = {}
        self.env_workspace = {}
        self.workspace = ''

    def build(self, workspace=None, aws_role=None, aws_account_id=None, aws_assume_role=None):
        if path.exists(CLI_ROOT + '/secrets'):
            self.env_auth = docker.utils.parse_env_file(CLI_ROOT + '/secrets')
        else:
            click.echo('Please login before proceeding')
            raise SystemExit

        self.workspace = workspace or getenv('WORKSPACE') or 'default'
        click.echo('Setting workspace to %s' % (self.workspace))

        aws_account_id = aws_account_id or get_workspace_value(self.workspace, 'aws.account_id')
        aws_role = aws_role or get_workspace_value(self.workspace, 'aws.role')
        aws_assume_role = aws_assume_role or get_workspace_value(self.workspace, 'aws.assume_role', 'false')

        self.env_workspace = {
            'TF_VAR_aws_role': aws_role,
            'TF_VAR_aws_account_id': aws_account_id,
            'WORKSPACE': self.workspace
        }

        if aws_assume_role.lower() == 'true':
            self.aws_assume_role(aws_role=aws_role, aws_account_id=aws_account_id)

        return self

    def aws_assume_role(self, aws_role, aws_account_id):
        click.echo('Assuming role %s at %s' % (aws_role, aws_account_id))
        container = Container()
        image = Image()

        AWS_IMAGE = image.get_image('aws')
        envs = {
            'AWS_ROLE': aws_role,
            'AWS_ACCOUNT_ID': aws_account_id,
        }
        envs.update(self.env_auth)

        command = 'assume-role.sh'
        output = container.create(
            image=AWS_IMAGE,
            entrypoint='/bin/bash -c',
            command=command,
            volumes=['.:/work'],
            environment=envs,
            tty=False,
            stdin_open=False
        )

        self.env_assume = parse_env('\n'.join(output.splitlines()))
        return self.env_assume

    def get_env(self):
        return {**self.env_auth, **self.env_assume, **self.env_workspace}
