import click
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment.aws import EnvironmentAws
from one.utils.terraform_modules import terraform_modules_check

image = Image()
container = Container()
environment = EnvironmentAws()
TERRAFORM_IMAGE = image.get_image('terraform')


@click.group(help='Group of terraform commands wrapped inside docker.')
def terraform():
    pass


@terraform.command(help='Run terraform init inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str, help='Workspace to use.')
@click.option('-r', '--aws-role', 'aws_role', default=None, type=str, help='AWS role to use.')
def init(workspace, aws_role):
    envs = environment.build(workspace, aws_role).get_env()

    container.create(
        image=TERRAFORM_IMAGE,
        command='init',
        volumes=['.:/work'],
        environment=envs
    )

    command_create_workspace = 'workspace new %s' % (envs['WORKSPACE'])
    container.create(
        image=TERRAFORM_IMAGE,
        command=command_create_workspace,
        volumes=['.:/work'],
        environment=envs
    )

    command_select_workspace = 'workspace "select" %s' % (envs['WORKSPACE'])
    container.create(
        image=TERRAFORM_IMAGE,
        command=command_select_workspace,
        volumes=['.:/work'],
        environment=envs
    )

    terraform_modules_check()


@terraform.command(help='Run terraform plan inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str, help='Workspace to use.')
@click.option('-r', '--aws-role', 'aws_role', default=None, type=str, help='AWS role to use.')
def plan(workspace, aws_role):
    envs = environment.build(workspace, aws_role).get_env()
    command = 'plan -out=.terraform-plan-' + envs['WORKSPACE']
    container.create(
        image=TERRAFORM_IMAGE,
        command=command,
        volumes=['.:/work'],
        environment=envs
    )


@terraform.command(help='Run terraform apply inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str, help='Workspace to use.')
@click.option('-r', '--aws-role', 'aws_role', default=None, type=str, help='AWS role to use.')
def apply(workspace, aws_role):
    envs = environment.build(workspace, aws_role).get_env()
    command = 'apply .terraform-plan-' + envs['WORKSPACE']
    container.create(
        image=TERRAFORM_IMAGE,
        command=command,
        volumes=['.:/work'],
        environment=envs
    )


@terraform.command(help='Run shell and get inside the container with interactive mode.')
@click.option('-w', '--workspace', default=None, type=str, help='Workspace to use.')
@click.option('-r', '--aws-role', 'aws_role', default=None, type=str, help='AWS role to use.')
def shell(workspace, aws_role):
    envs = environment.build(workspace, aws_role).get_env()
    container.create(
        image=TERRAFORM_IMAGE,
        entrypoint='/bin/bash',
        volumes=['.:/work'],
        environment=envs
    )


@terraform.command(help='Run terraform destroy inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str, help='Workspace to use.')
@click.option('-r', '--aws-role', 'aws_role', default=None, type=str, help='AWS role to use.')
def destroy(workspace, aws_role):
    envs = environment.build(workspace, aws_role).get_env()
    container.create(
        image=TERRAFORM_IMAGE,
        command='destroy',
        volumes=['.:/work'],
        environment=envs
    )


@terraform.command(help='Run terraform force-unlock inside the docker container.')
@click.argument('lock_id')
def force_unlock(lock_id):
    envs = environment.build().get_env()
    container.create(
        image=TERRAFORM_IMAGE,
        command='force-unlock',
        volumes=['.:/work'],
        environment=envs
    )
