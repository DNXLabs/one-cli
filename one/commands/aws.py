import click
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment.aws import EnvironmentAws


container = Container()
image = Image()
environment = EnvironmentAws()
AWS_IMAGE = image.get_image('aws')


@click.command(help='AWS CLI alias.')
@click.argument('args', nargs=-1)
@click.option('-w', '--workspace', default=None, type=str, help='Workspace to use.')
@click.option('-r', '--aws-role', 'aws_role', default=None, type=str, help='AWS role to use.')
def aws(args, workspace, aws_role):
    envs = environment.build(workspace, aws_role).get_env()
    command = ''
    for arg in args:
        command += '%s ' % (arg)
    container.create(
        image=AWS_IMAGE,
        command=command,
        volumes=['.:/work'],
        environment=envs
    )
