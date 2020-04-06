from one.docker.client import client
from one.utils.print_progress_bar import print_progress_bar
from os import path
import json
import yaml


GSUITE_AUTH_IMAGE = 'dnxsolutions/aws-google-auth:latest'
TERRAFORM_IMAGE = 'dnxsolutions/terraform:0.12.20-dnx1'
AZURE_AUTH_IMAGE = 'dnxsolutions/docker-aws-azure-ad:latest'


class Image:

    def __init__(self):
        pass


    def get_images(self):
        images = { 'terraform': TERRAFORM_IMAGE,
                   'gsuite': GSUITE_AUTH_IMAGE,
                   'azure': AZURE_AUTH_IMAGE }

        temp_images = {}
        if path.exists('./config.yaml'):
            with open('./config.yaml') as file:
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


    def get_tags(self, images):
        tags = []
        for image_tag in images.values():
            tags.append(image_tag)
        return tags


    def check(self):
        docker_images = client.images(all=True)
        count = 0

        desire_images = self.get_tags(self.get_images())
        desire_count = len(desire_images)

        for image in docker_images:
            if(image['RepoTags'][0] in desire_images):
                count += 1

        if count < desire_count:
            print('Your environment is missing some docker images')
            for image in desire_images:
                print('Checking image: ' + image)
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
                                               suffix=suffix)