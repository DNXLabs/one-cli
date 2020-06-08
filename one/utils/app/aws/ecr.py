from one.utils.config import get_config_value, get_workspace_value
from one.docker.image import Image
from one.docker.container import Container
from one.docker.image import Image
from one.docker.client import client as docker_client
from docker.errors import APIError
from .. import App

AWS_IMAGE = Image().get_image('aws')
container = Container()

class AppAwsEcr(App):
    def __init__(self):
        super().__init__()
        self.name = get_config_value('app.name')
        self.ecr_aws_region = get_config_value('app.docker.registry-options.ecr-aws-region')
        self.ecr_aws_account_id = get_config_value('app.docker.registry-options.ecr-aws-account-id')
        self.ecr_repository = get_config_value('app.docker.registry-options.ecr-repository', self.name)

    def get_image_name(self):
        registry_type = get_config_value('app.docker.registry-type', 'ecr')
        if registry_type == 'ecr':
            return "%s.dkr.ecr.%s.amazonaws.com/%s" % (self.ecr_aws_account_id, self.ecr_aws_region, self.ecr_repository)
        else:
            print('Docker registry "%s" not implemented' % registry_type)
        raise SystemExit

    def docker_login(self, envs):
        docker_get_login = container.create(
                image=AWS_IMAGE, 
                command="ecr get-login --no-include-email --registry-ids %s --region %s" % (self.ecr_aws_account_id, self.ecr_aws_region),
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

        print('ECR Docker login succeeded')