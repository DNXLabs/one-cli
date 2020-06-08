from one.utils.config import get_config_value
import subprocess

class App:
    def __init__(self):
        self.name = get_config_value('app.name')
        self.dockerfile = get_config_value('app.docker.file', 'Dockerfile')
        self.build_cmd_args = get_config_value('app.docker.build-cmd-args', '')

    def docker_build(self, build_version):
        image_tag = "%s:%s" % (self.name, build_version)
        command = ['docker', 'build', '-t', image_tag, '-f', self.dockerfile] + self.build_cmd_args.split(' ') + ['.']
        print(" ".join(command))
        subprocess.call(list(filter(None, command)))