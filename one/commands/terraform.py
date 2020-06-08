import click
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment.aws import EnvironmentAws

image = Image()
container = Container()
environment = EnvironmentAws()
TERRAFORM_IMAGE = image.get_image('terraform')


@click.group(help='Group of terraform commands wrapped inside docker.')
def terraform():
    pass


@terraform.command(help='Run terraform init inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str, help='Workspace to use')
def init(workspace):
    envs = environment.change_workspace(workspace).get_env()

    container.create(image=TERRAFORM_IMAGE, command='init', volumes=['.:/work'], environment=envs)

    command_create_workspace = 'workspace new %s' % (envs['WORKSPACE'])
    container.create(image=TERRAFORM_IMAGE, command=command_create_workspace, volumes=['.:/work'], environment=envs)

    command_select_workspace = 'workspace "select" %s' % (envs['WORKSPACE'])
    container.create(image=TERRAFORM_IMAGE, command=command_select_workspace, volumes=['.:/work'], environment=envs)


@terraform.command(help='Run terraform plan inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str, help='Workspace to use')
def plan(workspace):
    envs = environment.change_workspace(workspace).get_env()
    command = 'plan -out=.terraform-plan-' + envs['WORKSPACE']
    container.create(image=TERRAFORM_IMAGE, command=command, volumes=['.:/work'], environment=envs)


@terraform.command(help='Run terraform apply inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str, help='Workspace to use')
def apply(workspace):
    envs = environment.change_workspace(workspace).get_env()
    command = 'terraform apply .terraform-plan-' + envs['WORKSPACE']
    container.create(image=TERRAFORM_IMAGE, command=command, volumes=['.:/work'], environment=envs)


@terraform.command(help='Run shell and get inside the container with interactive mode.')
@click.option('-w', '--workspace', default=None, type=str, help='Workspace to use')
def shell(workspace):
    envs = environment.change_workspace(workspace).get_env()
    container.create(image=TERRAFORM_IMAGE, entrypoint='/bin/bash', volumes=['.:/work'], environment=envs)


@terraform.command(help='Run terraform destroy inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str, help='Workspace to use')
def destroy(workspace):
    envs = environment.change_workspace(workspace).get_env()
    container.create(image=TERRAFORM_IMAGE, command='destroy', volumes=['.:/work'], environment=envs)
