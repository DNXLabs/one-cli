import click
import subprocess
from one.utils.config import get_config_value
from one.docker.image import Image
from one.docker.container import Container
from one.utils.app import AppRegistry

AWS_IMAGE = Image().get_image('aws')
container = Container()


class AppRegistryEcr(AppRegistry):
    def __init__(self):
        super().__init__()
        self.name = get_config_value('app.name')
        self.ecr_aws_region = get_config_value('app.docker.registry-options.ecr-aws-region')
        self.ecr_aws_account_id = get_config_value('app.docker.registry-options.ecr-aws-account-id')

    def get_image_name(self, build_version):
        image_tag = super().get_image_tag(build_version)
        return "%s.dkr.ecr.%s.amazonaws.com/%s" % (self.ecr_aws_account_id, self.ecr_aws_region, image_tag)

    def docker_login(self, environment):
        if get_config_value('app.docker.registry-options.ecr-aws-assume-role', 'false').lower() == "true":
            aws_account_id = get_config_value('app.docker.registry-options.ecr-aws-account-id')
            aws_role = get_config_value('app.docker.registry-options.ecr-aws-role')
            environment.aws_assume_role(role=aws_role, account_id=aws_account_id)

        envs = environment.get_env()

        docker_get_login = container.create(
                image=AWS_IMAGE,
                command="ecr get-login --no-include-email --registry-ids %s --region %s" % (
                    self.ecr_aws_account_id, self.ecr_aws_region),
                environment=envs,
                tty=False)
        docker_login_command_parts = docker_get_login.strip().split(' ')
        # docker_login_username = docker_login_command_parts[3]
        # docker_login_password = docker_login_command_parts[5]
        # docker_login_endpoint = docker_login_command_parts[6]

        subprocess.call(list(filter(None, docker_login_command_parts)))

        # try:
        #     output = docker_client.login(username=docker_login_username,
        # password=docker_login_password, registry=docker_login_endpoint)
        # except APIError:
        #     click.echo('Error with docker login: ', docker_get_login.strip())
        #     raise SystemExit

        click.echo("Docker login succeeded: %s.dkr.ecr.%s.amazonaws.com" % (self.ecr_aws_account_id, self.ecr_aws_region))

    def docker_build(self, build_version):
        image = self.get_image_name(build_version)
        super().docker_build_raw(image)

    def docker_push(self, build_version):
        image = self.get_image_name(build_version)
        super().docker_push_raw(image)
