import dockerpty
from one.docker.client import client
from one.docker.image import Image
import os


class Container:

    def __init__(self):
        pass

    def create(self, image='', command=None, entrypoint=None, volumes=[],
               working_dir='/work', stdin_open=True, tty=True, environment=''):

        Image().check_image(image)
        host_config = None

        container_volumes = []
        binds = []
        for volume in volumes:
            volume_parts = volume.split(':')
            if volume_parts[0][0] == '.':
                volume_parts[0] = os.getcwd() + volume_parts[0][1:]
            container_volumes.append(volume_parts[1])
            binds.append(':'.join(volume_parts))

        host_config = client.create_host_config(binds=binds)

        container = client.create_container(image,
                                            command=command,
                                            entrypoint=entrypoint,
                                            stdin_open=stdin_open,
                                            tty=tty,
                                            environment=environment,
                                            working_dir=working_dir,
                                            volumes=container_volumes,
                                            host_config=host_config)

        if tty:
            dockerpty.start(client, container)
        else:
            client.start(container=container.get('Id'))
            client.wait(container=container.get('Id'))

        logs = client.logs(container['Id'])
        client.remove_container(container)

        return logs.decode('utf8')
