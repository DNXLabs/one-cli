import click
import sys
from one.docker.container import Container
from one.docker.image import Image
from one.__init__ import __version__


container = Container()
image = Image()


@click.command(help='Update CLI moving to latest stable version.')
def update():
    env = {}
    click.echo('Plataform: %s' % (sys.platform))
    click.echo('Updating CLI...')
    env['OSTYPE'] = sys.platform
    update_image = image.get_image('cli-update')
    bin_volume = '/usr/local/bin:/usr/local/bin'

    container.create(
        image=update_image,
        volumes=[bin_volume],
        environment=env,
        tty=False,
        stdin_open=False
    )
    click.echo('Update complete.\n')
    click.echo('one, version %s' % (__version__))
