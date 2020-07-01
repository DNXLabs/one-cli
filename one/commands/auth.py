import click
import shutil
import os
from PyInquirer import prompt
from one.docker.container import Container
from one.docker.image import Image
from one.utils.prompt import style
from one.utils.environment.idp import get_env_idp
from one.utils.environment.common import create_credential
from one.prompt.auth import AUTH_QUESTIONS, AWS_ACCESS_KEY_QUESTIONS
from one.__init__ import CLI_ROOT

container = Container()
image = Image()


@click.command(help='Authentication using SSO provider or AWS IAM user.')
def auth(auth_image=None):

    auth_answer = prompt(AUTH_QUESTIONS, style=style)
    if not auth_answer:
        raise SystemExit

    if auth_answer['auth'] == 'SSO':
        with open(CLI_ROOT + '/.env', 'w') as file:
            file.write('NONE=')
            file.close()

        env_idp = get_env_idp()

        if 'SSO' in env_idp:
            click.echo('Login with %s.\n' % (env_idp['SSO']))
            auth_image = image.get_image(env_idp['SSO'])
        else:
            click.echo('Invalid SSO configuration, removing config file.')
            os.remove(CLI_ROOT + '/idp')
            raise SystemExit

        credentials_volume = CLI_ROOT + ':/work'
        container.create(
            image=auth_image,
            volumes=[credentials_volume],
            environment=env_idp
        )

        shutil.move(CLI_ROOT + '/.env', CLI_ROOT + '/credentials')
    elif auth_answer['auth'] == 'AWS IAM user':
        aws_auth_answer = prompt(AWS_ACCESS_KEY_QUESTIONS, style=style)
        if not aws_auth_answer:
            raise SystemExit
        credential = {
            'AWS_ACCESS_KEY_ID': aws_auth_answer['AWS_ACCESS_KEY_ID'],
            'AWS_SECRET_ACCESS_KEY': aws_auth_answer['AWS_SECRET_ACCESS_KEY'],
            'REGION': aws_auth_answer['REGION']
        }
        create_credential(credential, CLI_ROOT + '/credentials')
    else:
        raise SystemExit
