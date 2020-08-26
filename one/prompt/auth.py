from one.utils.environment.common import get_credentials_file, get_config_file

DEFAULT_REGION = 'ap-southeast-2'

AWS_ACCESS_KEY_QUESTIONS = [
    {
        'type': 'input',
        'name': 'PROFILE',
        'default': 'default',
        'message': 'What\'s your profile name:',
        'validate': lambda text: len(text) >= 4 or 'Must be at least 4 characters.'
    },
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


def get_sso_profile_questions():
    aws_sso_auth_profiles = get_config_file().sections()

    if not aws_sso_auth_profiles:
        raise SystemExit

    aws_sso_auth_profiles = list(
                                map(
                                    lambda x: x.replace('profile ', ''),
                                    aws_sso_auth_profiles
                                )
                            )

    AWS_SSO_PROFILE_QUESTIONS = [
        {
            'type': 'list',
            'message': 'Select AWS SSO profile:',
            'name': 'profile',
            'choices': aws_sso_auth_profiles
        }
    ]

    return AWS_SSO_PROFILE_QUESTIONS


def get_iam_profile_questions():
    aws_iam_auth_profiles = get_credentials_file().sections()

    if not aws_iam_auth_profiles:
        raise SystemExit

    AWS_IAM_PROFILE_QUESTIONS = [
        {
            'type': 'list',
            'message': 'Select AWS IAM profile:',
            'name': 'profile',
            'choices': aws_iam_auth_profiles
        }
    ]

    return AWS_IAM_PROFILE_QUESTIONS
