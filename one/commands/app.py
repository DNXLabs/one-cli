import click
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment.aws import EnvironmentAws
from one.utils.config import get_config_value, get_workspace_value
from one.utils.app.common import app_deploy_factory, app_registry_factory

image = Image()
container = Container()
environment = EnvironmentAws()

ECS_DEPLOY_IMAGE = image.get_image('ecs_deploy')
AWS_IMAGE = image.get_image('aws')


@click.group(help='Group of app commands wrapped inside docker.')
def app():
    pass


@app.command(name='docker-build', help='Build docker image for deployment.')
@click.option('--build-version', default='latest', help='Build version, used as tag for docker image.')
def docker_build(build_version):
    app_registry = app_registry_factory(get_config_value('app.docker.registry_type', 'ecr'))
    app_registry.docker_build(build_version)


@app.command(name='docker-login', help='Login into docker registry.')
def docker_login():
    app_registry = app_registry_factory(get_config_value('app.docker.registry_type', 'ecr'))
    app_registry.docker_login(environment)


@app.command(name='docker-push', help='Push image to docker registry.')
@click.option('--build-version', default='latest', help='Build version, used as tag for docker image.')
def docker_push(build_version):
    app_registry = app_registry_factory(get_config_value('app.docker.registry_type', 'ecr'))
    app_registry.docker_push(build_version)


@app.command(name='deploy-ecs', help='Deploy application to ECS.')
@click.option('-w', '--workspace', required=True, help='Workspace to deploy.')
@click.option('--build-version', default='latest', help='Build version to deploy (default: latest).')
def deploy_ecs(workspace, build_version):
    app_deploy = app_deploy_factory(get_workspace_value(workspace, 'type', 'ecs'))
    app_registry = app_registry_factory(get_config_value('app.docker.registry_type', 'ecr'))

    environment.build(workspace)
    image_name = app_registry.get_image_name(build_version)

    click.echo('Deploying %s to %s' % (image_name, workspace))

    app_deploy.deploy(environment, workspace, image_name)


@app.command(name='deploy-static', help='Deploy static application to S3 bucket.')
@click.option('-w', '--workspace', default=None, help='Workspace to deploy.')
def deploy_static(workspace):
    app_deploy = app_deploy_factory('static')

    environments = environment.build(workspace).get_env()

    click.echo('Deploying static app to %s' % (environments.get('WORKSPACE', 'default')))

    app_deploy.deploy(environments)
