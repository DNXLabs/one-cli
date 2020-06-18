import click
import yaml
from one.docker.client import client
from one.utils.print_progress_bar import print_progress_bar
from one.__init__ import CONFIG_FILE
from os import path
from requests.exceptions import ConnectionError


GSUITE_AUTH_IMAGE = 'dnxsolutions/aws-google-auth:latest'
AZURE_AUTH_IMAGE = 'dnxsolutions/docker-aws-azure-ad:latest'
TERRAFORM_IMAGE = 'dnxsolutions/terraform:0.12.20-dnx1'
AWS_IMAGE = 'dnxsolutions/aws:1.18.44-dnx2'
ECS_DEPLOY_IMAGE = 'dnxsolutions/ecs-deploy:1.2.0'
CLI_UPDATE_IMAGE = 'dnxsolutions/one-cli-update:latest'


class Image:

    def __init__(self):
        pass

    def get_images(self):
        images = {'terraform': TERRAFORM_IMAGE,
                  'gsuite': GSUITE_AUTH_IMAGE,
                  'azure': AZURE_AUTH_IMAGE,
                  'aws': AWS_IMAGE,
                  'ecs-deploy': ECS_DEPLOY_IMAGE,
                  'cli-update': CLI_UPDATE_IMAGE}

        temp_images = {}
        if path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as file:
                docs = yaml.load(file, Loader=yaml.FullLoader)
                temp_images = docs['images']
            file.close()
            for key, value in temp_images.items():
                if value:
                    images.update({key: value})
        return images

    def get_image(self, key):
        images = self.get_images()
        return images[key]

    def check_image(self, image):
        try:
            docker_image = client.images(name=image, all=True)
        except ConnectionError:
            click.echo('Error: Make sure Docker is running (requests.exceptions.ConnectionError)')
            raise SystemExit

        if not docker_image:
            self.pull(image)

    def pull(self, image):
        for line in client.pull(image, stream=True, decode=True):
            if 'progressDetail' in line:
                progress_detail = line['progressDetail']
                if len(progress_detail) != 0:
                    current = progress_detail['current']
                    total = progress_detail['total']
                    prefix = line['id']
                    suffix = line['status']
                    print_progress_bar(iteration=current,
                                       total=total,
                                       prefix=prefix,
                                       suffix=suffix,
                                       fill='=')
