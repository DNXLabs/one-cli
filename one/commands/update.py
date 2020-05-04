import click
import requests
from sys import platform
from one.__init__ import __version__


url_linux_amd64 = 'https://github.com/DNXLabs/one-cli/releases/latest/download/one_linux_amd64'
url_macos_amd64 = 'https://github.com/DNXLabs/one-cli/releases/latest/download/one_macos_amd64'


@click.command(help='Update CLI moving to latest stable version.')
def update():
    url = ''
    print('Plataform: %s' % (platform))
    if platform == "linux" or platform == "linux2":
        url = url_linux_amd64
    elif platform == "darwin":
        url = url_macos_amd64

    file_name = '/usr/local/bin/one'
    with open(file_name, "wb") as f:
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')
        if total_length is None: # no content length header
                f.write(response.content)
        else:
            count = int(total_length)
            with click.progressbar(
                length=count,
                fill_char='='
            ) as bar:
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    bar.update(len(data))
    print('one, version %s' % (__version__))