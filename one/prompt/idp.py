prompt_providers = ['Google G Suite SSO', 'Microsoft Azure SSO', 'AWS SSO', 'AWS IAM user']

PROVIDER_QUESTIONS = [
    {
        'type': 'list',
        'message': 'Select authentication method:',
        'name': 'provider',
        'choices': prompt_providers
    }
]

GSUITE_QUESTIONS = [
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

AZURE_QUESTIONS = [
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
