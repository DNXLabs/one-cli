import json
import re
import click
import requests
from os import path


def terraform_modules_check():
    file_path = '.terraform/modules/modules.json'
    if not path.exists(file_path):
        raise SystemExit

    response = requests.get('https://modules.dnx.one/api.json')
    if response.status_code != 200:
        raise SystemExit
    api = response.json()

    with open('.terraform/modules/modules.json') as modules_json_file:
        data = json.load(modules_json_file)
        click.echo(
            click.style('\nInitializing DNX modules check...', bold=True)
        )
        for module in data['Modules']:

            if not module['Source']:
                continue

            split = re.split(r'[./]\s*', module['Source'])
            if len(split) >= 5 and split[4] == 'DNXLabs':
                try:
                    name = re.split(r'[./]\s*', module['Source'])[5]
                    version = module['Source'].split('=')[1]
                    key = module['Key']
                    api_version = ''
                    api_version = api['modules'][name]['tag_name']
                except (KeyError, IndexError):
                    click.echo(
                        click.style('ERROR ', fg='red') +
                        'Could not find module ' + name + ' at DNX modules API.'
                    )
                    continue

                if api_version != version:
                    click.echo(
                        '- ' + name + '/' + key + ': ' +
                        click.style(version, fg='yellow') +
                        ' ~> ' +
                        click.style(api_version, fg='green')
                    )
                else:
                    click.echo(
                        '- ' + name + '/' + key + ': ' +
                        click.style(version, fg='green')
                    )
