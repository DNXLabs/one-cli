import click
import docker.utils
from os import path
from PyInquirer import prompt
from one.utils.prompt import style
from one.utils.environment.common import create_credential
from one.__init__ import CLI_ROOT
from one.prompt.idp import PROVIDER_QUESTIONS, GSUITE_QUESTIONS, AZURE_QUESTIONS


def config_idp():
    provider_answer = prompt(PROVIDER_QUESTIONS, style=style)
    if not provider_answer:
        raise SystemExit

    if provider_answer['provider'] == 'Google G Suite':
        answers = prompt(GSUITE_QUESTIONS, style=style)
        if not bool(answers):
            raise SystemExit
        credential = {
            'SSO': 'gsuite',
            'GOOGLE_IDP_ID': answers['GOOGLE_IDP_ID'],
            'GOOGLE_SP_ID': answers['GOOGLE_SP_ID']
        }
        create_credential(credential, CLI_ROOT + '/idp')
    elif provider_answer['provider'] == 'Microsoft Azure':
        answers = prompt(AZURE_QUESTIONS, style=style)
        if not bool(answers):
            raise SystemExit
        credential = {
            'SSO': 'azure',
            'AZURE_TENANT_ID': answers['AZURE_TENANT_ID'],
            'AZURE_APP_ID_URI': answers['AZURE_APP_ID_URI']
        }
        create_credential(credential, CLI_ROOT + '/idp')
    else:
        raise SystemExit


def get_env_idp():
    if not path.exists(CLI_ROOT + '/idp'):
        click.echo('\nYou do not have any IDP configured, starting configuration.\n')
        config_idp()

    env_idp = docker.utils.parse_env_file(CLI_ROOT + '/idp')
    return env_idp
