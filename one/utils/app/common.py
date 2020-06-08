from one.utils.app.aws.ecr import AppAwsEcr


def app_factory(registry_type):
    if registry_type == 'ecr':
        return AppAwsEcr()
    else:
        print('Docker registry-type not implemented. Valid values: ecr')
        raise SystemExit
