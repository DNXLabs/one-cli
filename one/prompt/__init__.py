import click
import subprocess
from one.utils.config import get_config_value


class App:
    pass


class AppRegistry:
    def __init__(self):
        self.name = get_config_value('app.name')
        self.image_name = get_config_value('app.docker.image_name', get_config_value('app.name'))
        self.dockerfile = get_config_value('app.docker.file', 'Dockerfile')
        self.build_cmd_args = get_config_value('app.docker.build_cmd_args', '')

    def get_image_tag(self, build_version):
        return "%s:%s" % (self.image_name, build_version)

    def docker_build_raw(self, image):
        command = ['docker', 'build', '-t', image, '-f', self.dockerfile] + self.build_cmd_args.split(' ') + ['.']
        click.echo(" ".join(command))
        subprocess.call(list(filter(None, command)))

    def docker_push_raw(self, image):
        command = ['docker', 'push', image]
        click.echo(" ".join(command))
        subprocess.call(list(filter(None, command)))
