import click
from one.utils.app.registry.ecr import AppRegistryEcr
from one.utils.app.deploy.ecs import AppDeployEcs
from one.utils.app.deploy.static import AppDeployStatic


def app_deploy_factory(type):
    if type == 'ecs':
        return AppDeployEcs()
    elif type == 'static':
        return AppDeployStatic()
    else:
        click.echo('Type not implemented. Valid values: ecs, static.')
        raise SystemExit


def app_registry_factory(registry_type):
    if registry_type == 'ecr':
        return AppRegistryEcr()
    else:
        click.echo('Docker registry_type not implemented. Valid values: ecr')
        raise SystemExit
