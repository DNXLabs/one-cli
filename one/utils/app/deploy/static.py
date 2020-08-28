import click
import os
from one.utils.config import get_workspace_value, get_config_value
from one.docker.container import Container
from one.docker.image import Image
from one.utils.app import App

AWS_IMAGE = Image().get_image('aws')
container = Container()


class AppDeployStatic(App):
    def __init__(self):
        super().__init__()

    def deploy(self, environments):
        workspace = environments.get('WORKSPACE', 'default')

        env_deploy = {
            'AWS_DEFAULT_REGION': get_workspace_value(workspace, 'aws.region')
        }
        environments.update(env_deploy)

        s3_bucket_name = get_config_value('app.s3_bucket', '') or get_workspace_value(workspace, 'app.s3_bucket')
        distribution_id = get_config_value('app.distribution_id', '') or get_workspace_value(workspace, 'app.distribution_id')
        src_dir = get_config_value('app.src', '') or get_workspace_value(workspace, 'app.src')

        if not os.path.isdir(src_dir):
            click.echo('Source folder not found (%s)' % src_dir)
            raise SystemExit

        command_s3_sync = """s3 sync %s s3://%s --delete --cache-control \
                             max-age=31536000 --acl public-read""" % (src_dir, s3_bucket_name)
        container.create(
            command=command_s3_sync,
            image=AWS_IMAGE,
            environment=environments,
            volumes=['.:/work']
        )

        if distribution_id:
            command_cloudfront = 'cloudfront create-invalidation --distribution-id %s --paths "/*"' % (distribution_id)

            container.create(
                command=command_cloudfront,
                image=AWS_IMAGE,
                environment=environments,
                volumes=['.:/work']
            )
