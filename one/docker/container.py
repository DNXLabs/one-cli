import dockerpty
import docker.utils
import time
from one.docker.client import client
from one.docker.image import Image
import os


class Container:

    def __init__(self):
        pass


    def create(self, image='', command=None, entrypoint=None, stdin_open=True, tty=True, environment=''):
        docker_image = client.images(name=image, all=True)
        if not docker_image:
            Image().pull(image)

        container = client.create_container(image,
                                            command=command,
                                            entrypoint=entrypoint,
                                            stdin_open=stdin_open,
                                            tty=tty,
                                            environment=environment,
                                            working_dir='/work',
                                            volumes=['/work'],
                                            host_config=client.create_host_config(
                                                binds={ os.getcwd(): {
                                                    'bind': '/work',
                                                    'mode': 'rw',
                                                    }
                                                }
                                            ))

        if tty:
            dockerpty.start(client, container)

        logs = client.logs(container['Id'])

        client.remove_container(container)

        return logs