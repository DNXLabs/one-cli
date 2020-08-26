import click
import shutil
import configparser
import os
from os import path
from PyInquirer import prompt
from one.docker.container import Container
from one.docker.image import Image
from one.utils.prompt import style
from one.prompt.auth import get_sso_profile_questions, get_iam_profile_questions
from one.__init__ import CLI_ROOT
from one.utils.environment.common import create_secrets, get_credentials_file, get_config_file, get_idp_file
from one.utils.environment.idp import configure_idp, configure_gsuite, configure_azure, configure_aws_sso, configure_iam_user

container = Container()
image = Image()


@click.group(help='Group of auth commands.')
def auth():
    pass


@auth.command(help='Configure authentication to be used.')
def configure():
    configure_idp()


@auth.command(help='Authentication using SSO provider or AWS IAM user.')
def gsuite(auth_image=None):
    if not check_config_file(['idp']):
        configure_gsuite()
    auth_image = image.get_image('gsuite')

    with open(CLI_ROOT + '/.env', 'w') as file:
        file.write('NONE=')
        file.close()

    idp_file = get_idp_file()
    envs = {
        'GOOGLE_IDP_ID': idp_file['gsuite']['google_idp_id'],
        'GOOGLE_SP_ID': idp_file['gsuite']['google_sp_id']
    }

    credentials_volume = CLI_ROOT + ':/work'
    container.create(
        image=auth_image,
        volumes=[credentials_volume],
        environment=envs
    )

    shutil.move(CLI_ROOT + '/.env', CLI_ROOT + '/secrets')


@auth.command(help='Authentication using Azure SSO provider')
def azure():
    if not check_config_file(['idp']):
        configure_azure()
    auth_image = image.get_image('azure')
    credentials_volume = CLI_ROOT + ':/work'

    idp_file = get_idp_file()
    envs = {
        'AZURE_TENANT_ID': idp_file['azure']['azure_tenant_id'],
        'AZURE_APP_ID_URI': idp_file['azure']['azure_app_id_uri']
    }

    container.create(
        image=auth_image,
        volumes=[credentials_volume],
        environment=envs
    )

    shutil.move(CLI_ROOT + '/.env', CLI_ROOT + '/secrets')


@auth.command(help='Authentication using AWS SSO provider.')
def aws():
    if not check_config_file(['config']):
        configure_aws_sso()
    aws_sso_profile_answer = prompt(get_sso_profile_questions(), style=style)
    if not aws_sso_profile_answer:
        raise SystemExit

    auth_image = image.get_image('aws_v2')
    work_volume = CLI_ROOT + ':/work'
    envs = {
        'AWS_CONFIG_FILE': '/work/config',
        'AWS_SSO_PROFILE': aws_sso_profile_answer.get('profile', 'default')
    }

    container.create(
        image=auth_image,
        entrypoint='bash',
        command='/opt/scripts/aws-sso.sh',
        volumes=[work_volume],
        environment=envs
    )

    shutil.copy(CLI_ROOT + '/.env', CLI_ROOT + '/secrets')
    os.remove(CLI_ROOT + '/.env')


@auth.command(help='Authentication using AWS IAM user.')
def iam():
    if not check_config_file(['credentials', 'config']):
        configure_iam_user()
    aws_iam_profile_answer = prompt(get_iam_profile_questions(), style=style)

    if not aws_iam_profile_answer:
        raise SystemExit

    profile = aws_iam_profile_answer.get('profile', 'default')
    credentials_file = get_credentials_file()
    config_file = get_config_file()
    credential = {
        'AWS_ACCESS_KEY_ID': credentials_file[profile]['aws_access_key_id'],
        'AWS_SECRET_ACCESS_KEY': credentials_file[profile]['aws_secret_access_key'],
        'REGION': config_file['profile ' + profile]['region']
    }

    create_secrets(credential, CLI_ROOT + '/secrets')


def check_config_file(files: list):
    for file in files:
        file_path = '%s/%s' % (CLI_ROOT, file)
        if not path.exists(file_path):
            click.echo('\nYou do not have any %s configured, starting configuration.\n' % file)
            with open(file_path, 'w+'):
                return False

        config = configparser.ConfigParser()
        config.read(file_path)

        if not config.sections():
            click.echo('%s file is empty.\n' % file.capitalize())
            return False

    return True
