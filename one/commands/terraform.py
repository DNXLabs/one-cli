import click
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment import Environment

image = Image()
container = Container()
environment = Environment()
TERRAFORM_IMAGE = image.get_image('terraform')


@click.group(help='Group of terraform commands wrapped inside docker.')
def terraform():
    pass


@terraform.command(help='Run terraform init inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str)
def init(workspace):
    envs = environment.build()
    if workspace:
        envs['WORKSPACE'] = workspace
    container.create(image=TERRAFORM_IMAGE, command='init', volume='/work', environment=envs)

    command_create_workspace = 'workspace new %s' % (envs['WORKSPACE'])
    container.create(image=TERRAFORM_IMAGE, command=command_create_workspace, environment=envs)

    command_select_workspace = 'workspace "select" %s' % (envs['WORKSPACE'])
    container.create(image=TERRAFORM_IMAGE, command=command_select_workspace, environment=envs)


@terraform.command(help='Run terraform plan inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str)
def plan(workspace):
    envs = environment.build()
    if workspace:
        envs['WORKSPACE'] = workspace
    command = 'plan -out=.terraform-plan-' + envs['WORKSPACE']
    container.create(image=TERRAFORM_IMAGE, command=command, volume='/work', environment=envs)


@terraform.command(help='Run terraform apply inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str)
def apply(workspace):
    envs = environment.build()
    if workspace:
        envs['WORKSPACE'] = workspace
    command = 'terraform apply .terraform-plan-' + envs['WORKSPACE']
    container.create(image=TERRAFORM_IMAGE, command=command, volume='/work', environment=envs)


@terraform.command(help='Run shell and get inside the container with interactive mode.')
@click.option('-w', '--workspace', default=None, type=str)
def shell(workspace):
    envs = environment.build()
    if workspace:
        envs['WORKSPACE'] = workspace
    container.create(image=TERRAFORM_IMAGE, entrypoint='/bin/bash', volume='/work', environment=envs)


@terraform.command(help='Run terraform destroy inside the docker container.')
@click.option('-w', '--workspace', default=None, type=str)
def destroy(workspace):
    envs = environment.build()
    if workspace:
        envs['WORKSPACE'] = workspace
    container.create(image=TERRAFORM_IMAGE, command='destroy', volume='/work', environment=envs)
