import click
from one.utils.prompt import style
from PyInquirer import prompt
from one.utils.environment import home


@click.group(help='Manage the IDP configuration in your local.')
def idp():
    pass


@idp.command(help='Set IDP to be used.')
def config():
	prompt_providers = ['Google G Suite', 'Microsoft Azure']

	provider_questions = [
        {
            'type': 'list',
            'message': 'Select provider',
            'name': 'provider',
            'choices': prompt_providers
        }
    ]

	provider_answer = prompt(provider_questions, style=style)
	if not bool(provider_answer): # Empty answer
		raise SystemExit
	else:
		print()
		if provider_answer['provider'] == 'Google G Suite':
			gsuite_questions = [
				{
					'type': 'input',
					'name': 'GOOGLE_IDP_ID',
					'message': 'What\'s your GOOGLE_IDP_ID credential:',
					'validate': lambda text: len(text) >= 4 or 'Must be at least 4 characters.'
				},
				{
					'type': 'input',
					'name': 'GOOGLE_SP_ID',
					'message': 'What\'s your GOOGLE_SP_ID credential:',
					'validate': lambda text: len(text) >= 4 or 'Must be at least 4 characters.'
				}
			]
			answers = prompt(gsuite_questions, style=style)
			if not bool(answers): # Empty answer
				raise SystemExit
			credential = build_credential('GOOGLE_IDP_ID', answers['GOOGLE_IDP_ID'], 'GOOGLE_SP_ID', answers['GOOGLE_SP_ID'])
			create_creadential(credential)
		elif provider_answer['provider'] == 'Microsoft Azure':
			azure_questions = [
				{
					'type': 'input',
					'name': 'AZURE_TENANT_ID',
					'message': 'What\'s your AZURE_TENANT_ID credential:',
					'validate': lambda text: len(text) >= 4 or 'Must be at least 4 characters.'
				},
				{
					'type': 'input',
					'name': 'AZURE_APP_ID_URI',
					'message': 'What\'s your AZURE_APP_ID_URI credential:',
					'validate': lambda text: len(text) >= 4 or 'Must be at least 4 characters.'
				}
			]
			answers = prompt(azure_questions, style=style)
			if not bool(answers): # Empty answer
				raise SystemExit
			credential = build_credential('AZURE_TENANT_ID', answers['AZURE_TENANT_ID'], 'AZURE_APP_ID_URI', answers['AZURE_APP_ID_URI'])
			create_creadential(credential)
		else:
			raise SystemExit


def build_credential(key1, value1, key2, value2):
	return '%s=%s\n%s=%s\n' % (key1, value1, key2, value2)


def create_creadential(credential):
	with open(home + '/.one/idp', 'w+') as f:
		f.write(credential)
		f.close()