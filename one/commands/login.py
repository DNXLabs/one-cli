import click
import shutil
import os
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment.idp import get_env_idp
from one.__init__ import CLI_ROOT

container = Container()
image = Image()


@click.command(help='Login using your configured SSO provider.')
def login(auth_image=None):
    f = open('.env', 'w')
    f.write('NONE=')
    f.close()

    env_idp = get_env_idp()

    if 'SSO' in env_idp:
        click.echo('Login with %s.\n' % (env_idp['SSO']))
        auth_image = image.get_image(env_idp['SSO'])
    else:
        click.echo('Invalid SSO configuration, removing config file.')
        os.remove(CLI_ROOT + '/idp')
        raise SystemExit

    container.create(
        image=auth_image,
        volumes=['.:/work'],
        environment=env_idp
    )

    shutil.move('.env', CLI_ROOT + '/credentials')
