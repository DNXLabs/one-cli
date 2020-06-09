import click
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment.aws import EnvironmentAws
from one.utils.config import get_config_value, get_workspace_value
from one.utils.app.common import app_deploy_factory, app_registry_factory

image = Image()
container = Container()
environment = EnvironmentAws()

ECS_DEPLOY_IMAGE = image.get_image('ecs-deploy')
AWS_IMAGE = image.get_image('aws')


@click.group(help='Group of app commands wrapped inside docker.')
def app():
    pass


@app.command(name='docker-build', help='Build docker image for deployment')
@click.option('--build-version', default='latest', help='Build version, used as tag for docker image')
def docker_build(build_version):
    app_registry = app_registry_factory(get_config_value('app.docker.registry-type', 'ecr'))
    app_registry.docker_build(build_version)


@app.command(name='docker-login', help='Login into docker registry')
def docker_login():
    app_registry = app_registry_factory(get_config_value('app.docker.registry-type', 'ecr'))
    app_registry.docker_login(environment)


@app.command(name='docker-push', help='Push image to docker registry')
@click.option('--build-version', default='latest', help='Build version, used as tag for docker image')
def docker_push(build_version):
    app_registry = app_registry_factory(get_config_value('app.docker.registry-type', 'ecr'))
    app_registry.docker_push(build_version)


@app.command(name='deploy', help='Deploy application')
@click.option('-w', '--workspace', required=True, help='Workspace to deploy')
@click.option('--build-version', default='latest', help='Build version to deploy (default: latest)')
def deploy(workspace, build_version):
    app_deploy = app_deploy_factory(get_workspace_value(workspace, 'type', 'ecs'))
    app_registry = app_registry_factory(get_config_value('app.docker.registry-type', 'ecr'))

    environment.change_workspace(workspace)
    image_name = app_registry.get_image_name(build_version)

    print('Deploying %s to %s' % (image_name, workspace))

    app_deploy.deploy(environment, workspace, image_name)