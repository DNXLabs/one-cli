import dockerpty
import docker.utils
from one.docker.client import client
import os


class Container:

    def __init__(self):
        pass


    def create(self, image='', command=None, entrypoint=None, stdin_open=True, tty=True, environment=''):
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
										)
				)
        dockerpty.start(client, container)
        client.remove_container(container)