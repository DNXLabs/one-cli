import click
import shutil
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment.common import get_env_idp, get_cli_root

container = Container()
image = Image()


@click.group(help='Group of commands to login specifying one SSO provider.')
def login():
    pass


@login.command(help='Login with GSuite.')
def gsuite():
    f = open('.env', 'w')
    f.write('NONE=')
    f.close()

    env_idp = get_env_idp()
    gsuite_auth_image = image.get_image('gsuite')
    container.create(
        image=gsuite_auth_image,
        volumes=['.:/work'],
        environment=env_idp
    )

    shutil.move('.env', get_cli_root() + '/credentials')


@login.command(help='Login with Azure.')
def azure():
    f = open('.env', 'w')
    f.write('NONE=')
    f.close()

    env_idp = get_env_idp()
    azure_auth_image = image.get_image('azure')
    container.create(
        image=azure_auth_image,
        volumes=['.:/work'],
        environment=env_idp
    )

    shutil.move('.env', get_cli_root() + '/credentials')
