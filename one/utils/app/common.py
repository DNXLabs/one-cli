from one.utils.app.registry.ecr import AppRegistryEcr
from one.utils.app.deploy.ecs import AppDeployEcs


def app_deploy_factory(type):
    if type == 'ecs':
        return AppDeployEcs()
    else:
        print('Type not implemented. Valid values: ecs')
        raise SystemExit


def app_registry_factory(registry_type):
    if registry_type == 'ecr':
        return AppRegistryEcr()
    else:
        print('Docker registry-type not implemented. Valid values: ecr')
        raise SystemExit
