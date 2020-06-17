import click
import docker.utils
from os import path
from PyInquirer import prompt
from one.utils.prompt import style
from one.__init__ import CLI_ROOT
from one.prompt.idp import PROVIDER_QUESTIONS, GSUITE_QUESTIONS, AZURE_QUESTIONS


def config_idp():
    provider_answer = prompt(PROVIDER_QUESTIONS, style=style)
    if not bool(provider_answer):
        raise SystemExit
    else:
        if provider_answer['provider'] == 'Google G Suite':
            answers = prompt(GSUITE_QUESTIONS, style=style)
            if not bool(answers):
                raise SystemExit
            credential = build(
                'SSO',
                'gsuite',
                'GOOGLE_IDP_ID',
                answers['GOOGLE_IDP_ID'],
                'GOOGLE_SP_ID',
                answers['GOOGLE_SP_ID']
            )
            create(credential)
        elif provider_answer['provider'] == 'Microsoft Azure':
            answers = prompt(AZURE_QUESTIONS, style=style)
            if not bool(answers):
                raise SystemExit
            credential = build(
                'SSO',
                'azure',
                'AZURE_TENANT_ID',
                answers['AZURE_TENANT_ID'],
                'AZURE_APP_ID_URI',
                answers['AZURE_APP_ID_URI']
            )
            create(credential)
        else:
            raise SystemExit


def build(key1, value1, key2, value2, key3, value3):
    return '%s=%s\n%s=%s\n%s=%s\n' % (key1, value1, key2, value2, key3, value3)


def create(credential):
    with open(CLI_ROOT + '/idp', 'w+') as f:
        f.write(credential)
        f.close()


def get_env_idp():
    if not path.exists(CLI_ROOT + '/idp'):
        click.echo('You do not have any IDP configured, starting configuration.\n')
        config_idp()

    env_idp = docker.utils.parse_env_file(CLI_ROOT + '/idp')
    return env_idp
