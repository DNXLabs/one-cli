import click
from one.docker.container import Container
from one.docker.image import Image
from one.utils.environment import Environment
from one.utils.config import get_config_value
import subprocess

image = Image()
container = Container()
environment = Environment()

TERRAFORM_IMAGE = image.get_image('terraform')


@click.group(help='Group of app commands wrapped inside docker.')
def app():
    pass

@app.command("docker-build", help='Build docker image for deployment')
@click.option('--tag_name', default='latest', help='Tag for image')
def docker_build(tag_name):
    app_name = get_config_value('app.name')
    dockerfile = get_config_value('app.docker.file', 'Dockerfile')
    build_cmd_args = get_config_value('app.docker.build-cmd-args', '')
    image_tag = "%s:%s" % (app_name, tag_name)

    command = ['docker', 'build', '-t', image_tag, '-f', dockerfile] + build_cmd_args.split(' ') + ['.']
    print(" ".join(command))
    subprocess.call(list(filter(None, command)))