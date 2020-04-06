import click
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment import Environment


TERRAFORM_IMAGE = Image().get_image('terraform')


@click.group(help='Group of terraform commands wrapped inside docker.')
def terraform():
    pass


@terraform.command(help='Run terraform init inside the docker container.')
def init():
    envs = Environment().build()
    Container().create(image=TERRAFORM_IMAGE, command='init', environment=envs)

    command_create_workspace = 'workspace new %s' % (envs['WORKSPACE'])
    Container().create(image=TERRAFORM_IMAGE, command=command_create_workspace, environment=envs)

    command_select_workspace = 'workspace "select" %s' % (envs['WORKSPACE'])
    Container().create(image=TERRAFORM_IMAGE, command=command_select_workspace, environment=envs)


@terraform.command(help='Run terraform plan inside the docker container.')
def plan():
    envs = Environment().build()
    command = 'plan -out=.terraform-plan-' + envs['WORKSPACE']
    Container().create(image=TERRAFORM_IMAGE, command=command, environment=envs)


@terraform.command(help='Run terraform apply inside the docker container.')
def apply():
    envs = Environment().build()
    command = 'terraform apply .terraform-plan-' + envs['WORKSPACE']
    Container().create(image=TERRAFORM_IMAGE, command=command, environment=envs)


@terraform.command(help='Run shell and get inside the container with interactive mode.')
def shell():
    envs = Environment().build()
    Container().create(image=TERRAFORM_IMAGE, entrypoint='/bin/bash', environment=envs)\


@terraform.command(help='Run terraform destroy inside the docker container.')
def destroy():
    envs = Environment().build()
    Container().create(image=TERRAFORM_IMAGE, command='destroy', environment=envs)