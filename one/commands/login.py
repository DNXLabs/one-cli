import click
import shutil
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment import get_env_idp, home


@click.group(help='Group of commands to login specifying one SSO provider.')
def login():
    pass


@login.command(help='Login with GSuite.')
def gsuite():
    f = open('.env', 'w')
    f.write('NONE=')
    f.close()

    env_idp = get_env_idp()
    gsuite_auth_image = Image().get_image('gsuite')
    Container().create(image=gsuite_auth_image, command=None, environment=env_idp)

    shutil.move('.env', home + '/.one/credentials')


@login.command(help='Login with Azure.')
def azure():
    f = open('.env', 'w')
    f.write('NONE=')
    f.close()

    env_idp = get_env_idp()
    azure_auth_image = Image().get_image('azure')
    Container().create(image=azure_auth_image, command=None, environment=env_idp)

    shutil.move('.env', home + '/.one/credentials')