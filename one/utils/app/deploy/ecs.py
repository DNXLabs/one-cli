import click
import os
from one.utils.config import get_config_value, get_workspace_value
from one.docker.container import Container
from one.docker.image import Image
from one.utils.app import App

ECS_DEPLOY_IMAGE = Image().get_image('ecs_deploy')
container = Container()


class AppDeployEcs(App):
    def __init__(self):
        super().__init__()

    def deploy(self, environment, workspace, image_name):
        env_deploy = {
            'AWS_DEFAULT_REGION': get_workspace_value(workspace, 'aws.region'),
            'APP_NAME': get_config_value('app.name'),
            'CLUSTER_NAME': get_workspace_value(workspace, 'ecs_cluster_name'),
            'CONTAINER_PORT': get_config_value('app.port'),
            'IMAGE_NAME': image_name,
        }

        ecs_task_definition_file = get_config_value('app.ecs_task_definition_file', 'task-definition.tpl.json')
        if not os.path.isfile(ecs_task_definition_file):
            click.echo('ECS task definition file not found (%s)' % ecs_task_definition_file)
            raise SystemExit

        envs = environment.get_env()

        timeout = get_workspace_value(workspace, 'deploy_timeout', '0')
        if timeout != '0':
            env_deploy['DEPLOY_TIMEOUT'] = timeout

        envs.update(env_deploy)
        container.create(
            image=ECS_DEPLOY_IMAGE,
            environment=envs,
            volumes=[
                './%s:/work/task-definition.tpl.json' % (ecs_task_definition_file)
            ]
        )
