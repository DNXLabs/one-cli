import json
import re
import click
import requests
from os import path


def get_modules_list(url='https://modules.dnx.one/api.json'):
    response = requests.get(url)
    if response.status_code != 200:
        raise SystemExit
    return response.json()


def check_file_path(file_path):
    if not path.exists(file_path):
        raise SystemExit


def terraform_modules_check(file_path='.terraform/modules/modules.json', api=None):
    check_file_path(file_path)

    json_api = api or get_modules_list()

    results = {}

    with open(file_path) as modules_json_file:
        data = json.load(modules_json_file)
        click.echo(
            click.style('\nInitializing DNX modules check...', bold=True)
        )
        try:
            for module in data['Modules']:

                if not module['Source']:
                    continue
                split = re.split(r'[./]\s*', module['Source'])
                if len(split) >= 5 and split[4] == 'DNXLabs':
                    name = re.split(r'[./]\s*', module['Source'])[5]
                    version = module['Source'].split('=')[1]
                    key = module['Key']
                    api_version = ''
                    try:
                        api_version = json_api['modules'][name]['tag_name']
                    except KeyError:
                        click.echo(
                            click.style('ERROR ', fg='red') +
                            'Could not find module ' + name + ' at DNX modules API.'
                        )
                    if api_version != version:
                        results[name] = {"key": key, "version": version, "api_version": api_version}
                        click.echo(
                            '- ' + name + '/' + key + ': ' +
                            click.style(version, fg='yellow') +
                            ' ~> ' +
                            click.style(api_version, fg='green')
                        )
                    else:
                        results[name] = {"key": key, "version": version}
                        click.echo(
                            '- ' + name + '/' + key + ': ' +
                            click.style(version, fg='green')
                        )
        except KeyError:
            click.echo(
                click.style('ERROR ', fg='red') +
                'Couldn not find data from local terraform modules'
            )
    return results
