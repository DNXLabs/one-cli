from one.docker.image import AZURE_AUTH_IMAGE, GSUITE_AUTH_IMAGE, TERRAFORM_IMAGE


CREATION_QUESTION = [
    {
        'type': 'input',
        'name': 'create',
        'message': 'Do you want to create workspaces now? [Y/n]',
        'default': 'Y'
    }
]


IMAGE_QUESTIONS = [
    {
        'type': 'input',
        'name': 'terraform',
        'default': TERRAFORM_IMAGE,
        'message': 'Terraform docker image:',
        'validate': lambda text: len(text) >= 4 or 'Must be at least 4 character.'
    },
    {
        'type': 'input',
        'name': 'gsuite',
        'default': GSUITE_AUTH_IMAGE,
        'message': 'G Suite docker image:',
        'validate': lambda text: len(text) >= 4 or 'Must be at least 4 character.'
    },
    {
        'type': 'input',
        'name': 'azure',
        'default': AZURE_AUTH_IMAGE,
        'message': 'Azure docker image:',
        'validate': lambda text: len(text) >= 4 or 'Must be at least 4 character.'
    },
]


WORKSPACE_QUESTIONS = [
    {
        'type': 'input',
        'name': 'AWS_ACCOUNT_ID',
        'message': 'What\'s your AWS_ACCOUNT_ID credential:',
        'validate': lambda text: len(text) >= 1 or 'Must be at least 1 character.'
    },
    {
        'type': 'input',
        'name': 'AWS_ROLE',
        'message': 'What\'s your AWS_ROLE credential:',
        'validate': lambda text: len(text) >= 1 or 'Must be at least 1 character.'
    },
    {
        'type': 'input',
        'name': 'WORKSPACE',
        'message': 'What\'s your WORKSPACE credential:',
        'validate': lambda text: len(text) >= 1 or 'Must be at least 1 character.'
    },
    {
        'type': 'input',
        'name': 'assume_role',
        'default': 'n',
        'message': 'Do you want to this workspace to assume role? [Y/n]'
    },
    {
        'type': 'input',
        'name': 'new_workspace',
        'default': 'Y',
        'message': 'Do you want to create another workspace? [Y/n]'
    }
]
