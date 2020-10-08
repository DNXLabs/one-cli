import click
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment.aws import EnvironmentAws


container = Container()
image = Image()
environment = EnvironmentAws()
SHELL_IMAGE = image.get_image('shell')


@click.command(help='Shell container with awscli and terraform pre-installed.')
@click.argument('args', nargs=-1)
@click.option('-i', '--image', default=SHELL_IMAGE, type=str, help='Docker image to use.')
@click.option('-p', '--port', default=(), type=str, help='Ports to expose from the container.', multiple=True)
def shell(args, image, port):
    envs = environment.build().get_env()
    command = ''

    for arg in args:
        command += '%s ' % (arg)

    ports = list(port)

    container.create(
        image=image,
        command=command,
        ports=ports,
        entrypoint='',
        volumes=['.:/work'],
        environment=envs
    )
