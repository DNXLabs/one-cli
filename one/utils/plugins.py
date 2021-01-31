import importlib
import sys
import subprocess
import click
import yaml
import importlib.util
from one.utils.config import get_config_value
from one.__init__ import CONFIG_FILE


def cleanup(garbage_packages):
    for garbage in garbage_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", garbage, "-y"])
        except subprocess.CalledProcessError:
            raise SystemExit


def get_installed_packages():
    try:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.decode() for r in reqs.split()]
        return installed_packages
    except subprocess.CalledProcessError:
        raise SystemExit


def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        raise SystemExit


def load_plugins():
    installed_packages = get_installed_packages()
    garbage_packages = [i for i in installed_packages if 'one-cli-plugin-' in i]
    try:
        with open(CONFIG_FILE) as file:
            docs = yaml.load(file, Loader=yaml.BaseLoader)
            for key, value in docs['plugins'].items():
                package = get_config_value('plugins.'+ key +'.package')
                module = get_config_value('plugins.'+ key +'.module')

                if package not in installed_packages:
                    click.echo('Installing plugin %s.' % package)
                    install(package)
                    click.echo('Plugin %s successfully installed.\n' % package)
                else:
                    garbage_packages.remove(package)

                getattr(importlib.import_module(module), '__init__')()

        file.close()
    except KeyError:
        pass
    except AttributeError:
        click.echo(
            click.style('ERROR ', fg='red') +
            'Plugin attribute error.\n'
        )
        raise SystemExit
    except FileNotFoundError:
        click.echo(
            click.style('ERROR ', fg='red') +
            'Config file %s not found.\n' % CONFIG_FILE
        )
    except Exception:
        click.echo(
            click.style('ERROR ', fg='red') +
            'Unexpected error.\n'
        )
        raise SystemExit

    cleanup(garbage_packages)
