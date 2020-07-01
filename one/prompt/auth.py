auth_types = ['SSO', 'AWS IAM user']

DEFAULT_REGION = 'ap-southeast-2'

AUTH_QUESTIONS = [
    {
        'type': 'list',
        'message': 'Select authentication type:',
        'name': 'auth',
        'choices': auth_types
    }
]

AWS_ACCESS_KEY_QUESTIONS = [
    {
        'type': 'input',
        'name': 'AWS_ACCESS_KEY_ID',
        'message': 'What\'s your AWS_ACCESS_KEY_ID:',
        'validate': lambda text: len(text) >= 4 or 'Must be at least 4 characters.'
    },
    {
        'type': 'input',
        'name': 'AWS_SECRET_ACCESS_KEY',
        'message': 'What\'s your AWS_SECRET_ACCESS_KEY:',
        'validate': lambda text: len(text) >= 4 or 'Must be at least 4 characters.'
    },
    {
        'type': 'input',
        'name': 'REGION',
        'default': DEFAULT_REGION,
        'message': 'What\'s your default REGION:',
        'validate': lambda text: len(text) >= 4 or 'Must be at least 4 characters.'
    }
]
