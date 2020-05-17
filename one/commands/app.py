import click
from one.docker.container import Container
from one.docker.image import Image
from one.docker.client import client as docker_client
from one.utils.environment import Environment
from one.utils.config import get_config_value, get_workspace_value
from docker.errors import APIError
import subprocess

image = Image()
container = Container()
environment = Environment()

ECS_DEPLOY_IMAGE = image.get_image('ecs-deploy')
AWS_IMAGE = image.get_image('aws')


@click.group(help='Group of app commands wrapped inside docker.')
def app():
    pass


@app.command(name='docker-build', help='Build docker image for deployment')
@click.option('--build-version', default='latest', help='Build version, used as tag for docker image')
def docker_build(build_version):
    app_name = get_config_value('app.name')
    dockerfile = get_config_value('app.docker.file', 'Dockerfile')
    build_cmd_args = get_config_value('app.docker.build-cmd-args', '')
    image_tag = "%s:%s" % (app_name, build_version)

    command = ['docker', 'build', '-t', image_tag, '-f', dockerfile] + build_cmd_args.split(' ') + ['.']
    print(" ".join(command))
    subprocess.call(list(filter(None, command)))


@app.command(name='docker-login', help='Login into docker registry')
def docker_login():
    envs = environment.build()

    if get_config_value('app.docker.registry-type', 'ecr') == 'ecr': 
        ecr_aws_region = get_config_value('app.docker.registry-options.ecr-aws-region')
        ecr_aws_account_id = get_config_value('app.docker.registry-options.ecr-aws-account-id')
        docker_get_login = container.create(
            image=AWS_IMAGE, 
            command="ecr get-login --no-include-email --registry-ids %s --region %s" % (ecr_aws_account_id, ecr_aws_region),
            environment=envs,
            tty=False)
        docker_login_command_parts = docker_get_login.strip().split(' ')
        docker_login_username = docker_login_command_parts[3]
        docker_login_password = docker_login_command_parts[5]
        docker_login_endpoint = docker_login_command_parts[6]

        try:
            output = docker_client.login(username=docker_login_username, password=docker_login_password, registry=docker_login_endpoint)
        except APIError:
            print('Error with docker login: ', docker_get_login.strip())
            raise SystemExit

        print('Login succeeded')
    else:
        print('Docker registry-type not implemented. Valid values: ecr')
        raise SystemExit


@app.command(name='deploy', help='Deploy application')
@click.option('--workspace', help='Workspace to deploy')
@click.option('--build-version', default='latest', help='Build version to deploy')
def deploy(workspace, build_version,):
    envs = environment.build(workspace)
    env_deploy = {}

    env_deploy['AWS_DEFAULT_REGION'] = get_workspace_value(workspace, 'aws-region')
    env_deploy['APP_NAME'] = get_config_value('app.name')
    env_deploy['CLUSTER_NAME'] = get_workspace_value(workspace, 'ecs-cluster-name')
    env_deploy['CONTAINER_PORT'] = get_config_value('app.port')

    ecr_aws_region = get_config_value('app.docker.ecr-aws-region')
    ecr_aws_account_id = get_config_value('app.docker.aws-account-id')
    ecr_repository = get_config_value('app.docker.ecr-repository', get_config_value('app.name'))
    env_deploy['IMAGE_NAME'] = "%s.dkr.ecr.%s.amazonaws.com/%s" % (ecr_aws_account_id, ecr_aws_region, ecr_repository)

    timeout = get_workspace_value(workspace, 'deploy-timeout', 0)
    if timeout != 0:
        env_deploy['DEPLOY_TIMEOUT'] = timeout

    envs.update(env_deploy)
    container.create(image=ECS_DEPLOY_IMAGE, environment=envs)
