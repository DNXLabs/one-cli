import click
from PyInquirer import prompt
from one.utils.environment.common import get_credentials_file, get_config_file, get_idp_file, write_config
from one.utils.prompt import style
from one.docker.image import Image
from one.docker.container import Container
from one.__init__ import CLI_ROOT
from one.prompt.idp import PROVIDER_QUESTIONS, GSUITE_QUESTIONS, AZURE_QUESTIONS, OKTA_QUESTIONS
from one.prompt.auth import AWS_ACCESS_KEY_QUESTIONS

image = Image()
container = Container()


def configure_idp():
    provider_answer = prompt(PROVIDER_QUESTIONS, style=style)
    if not provider_answer:
        raise SystemExit

    if provider_answer['provider'] == 'Google G Suite SSO':
        configure_gsuite()
    elif provider_answer['provider'] == 'Microsoft Azure SSO':
        configure_azure()
    elif provider_answer['provider'] == 'Okta SSO':
        configure_okta()
    elif provider_answer['provider'] == 'AWS SSO':
        configure_aws_sso()
    elif provider_answer['provider'] == 'AWS IAM user':
        configure_iam_user()
    else:
        raise SystemExit


def configure_gsuite():
    answers = prompt(GSUITE_QUESTIONS, style=style)
    if not bool(answers):
        raise SystemExit
    idp_file = get_idp_file()
    idp_file['gsuite'] = {
        'google_idp_id': answers['GOOGLE_IDP_ID'],
        'google_sp_id': answers['GOOGLE_SP_ID']
    }

    write_config(idp_file, '/idp')
    click.echo('\n')


def configure_azure():
    answers = prompt(AZURE_QUESTIONS, style=style)
    if not bool(answers):
        raise SystemExit

    idp_file = get_idp_file()
    idp_file['azure'] = {
        'AZURE_TENANT_ID': answers['AZURE_TENANT_ID'],
        'AZURE_APP_ID_URI': answers['AZURE_APP_ID_URI']
    }

    write_config(idp_file, '/idp')
    click.echo('\n')


def configure_okta():
    answers = prompt(OKTA_QUESTIONS, style=style)
    if not bool(answers):
        raise SystemExit
    idp_file = get_idp_file()
    idp_file['okta'] = {
        'okta_org': answers['OKTA_ORG'],
        'okta_aws_app_url': answers['OKTA_AWS_APP_URL'],
        'okta_aws_default_region': answers['OKTA_AWS_DEFAULT_REGION']
    }

    write_config(idp_file, '/idp')
    click.echo('\n')


def configure_aws_sso():
    auth_image = image.get_image('aws_v2')
    work_volume = CLI_ROOT + ':/work'
    env_sso = {}
    env_sso['AWS_CONFIG_FILE'] = '/work/config'

    container.create(
        image=auth_image,
        command='configure sso',
        volumes=[work_volume],
        environment=env_sso
    )
    click.echo('\n')


def configure_iam_user():
    aws_auth_answer = prompt(AWS_ACCESS_KEY_QUESTIONS, style=style)
    if not aws_auth_answer:
        raise SystemExit
    credentials_file = get_credentials_file()
    credentials_file[aws_auth_answer['PROFILE']] = {
        'AWS_ACCESS_KEY_ID': aws_auth_answer['AWS_ACCESS_KEY_ID'],
        'AWS_SECRET_ACCESS_KEY': aws_auth_answer['AWS_SECRET_ACCESS_KEY']
    }

    config_file = get_config_file()
    config_file['profile ' + aws_auth_answer['PROFILE']] = {
        'REGION': aws_auth_answer['REGION']
    }

    write_config(credentials_file, '/credentials')
    write_config(config_file, '/config')
    click.echo('\n')
