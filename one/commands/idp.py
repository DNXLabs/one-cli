import click
from one.utils.prompt import style
from PyInquirer import prompt
from one.utils.environment.common import home
from one.__init__ import CLI_ROOT
from one.prompt.idp import PROVIDER_QUESTIONS, GSUITE_QUESTIONS, AZURE_QUESTIONS


@click.group(help='Manage the IDP configuration in your local.')
def idp():
    pass


@idp.command(help='Set IDP to be used.')
def config():
    provider_answer = prompt(PROVIDER_QUESTIONS, style=style)
    if not bool(provider_answer):
        raise SystemExit
    else:
        print()
        if provider_answer['provider'] == 'Google G Suite':
            answers = prompt(GSUITE_QUESTIONS, style=style)
            if not bool(answers):
                raise SystemExit
            credential = build_credential(
                'GOOGLE_IDP_ID',
                answers['GOOGLE_IDP_ID'],
                'GOOGLE_SP_ID',
                answers['GOOGLE_SP_ID']
            )
            create_credential(credential)
        elif provider_answer['provider'] == 'Microsoft Azure':
            answers = prompt(AZURE_QUESTIONS, style=style)
            if not bool(answers):
                raise SystemExit
            credential = build_credential(
                'AZURE_TENANT_ID',
                answers['AZURE_TENANT_ID'],
                'AZURE_APP_ID_URI',
                answers['AZURE_APP_ID_URI']
            )
            create_credential(credential)
        else:
            raise SystemExit


def build_credential(key1, value1, key2, value2):
    return '%s=%s\n%s=%s\n' % (key1, value1, key2, value2)


def create_credential(credential):
    with open(home + CLI_ROOT + '/idp', 'w+') as f:
        f.write(credential)
        f.close()
