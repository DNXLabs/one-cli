import glob
import importlib
import sys
import os
import click
import json
import tarfile
import shutil
import yaml
from os.path import join
from os import path
import urllib.request
from pathlib import Path
from one.utils.config import get_config_value
from one.__init__ import CONFIG_FILE


home = str(Path.home())
TEMP_FOLDER = '.one/.temp'
PLUGIN_DATA_FILE = '.one/plugins.json'


def download_plugin(extract_source, url, key):
    file_stream = urllib.request.urlopen(url)

    if url.endswith('tar.gz'):
        tar = tarfile.open(fileobj=file_stream, mode='r|gz')
        tar.extractall(TEMP_FOLDER)
        tar.close()
    elif url.endswith('tar'):
        tar = tarfile.open(fileobj=file_stream, mode='r|')
        tar.extractall(TEMP_FOLDER)
        tar.close()
    else:
        click.echo(
            click.style('ERROR ', fg='red') +
            'No supporot for this file format.\n'
        )
        raise SystemExit

    plugin_path = join(extract_source, key)
    if path.exists(plugin_path):
        shutil.rmtree(plugin_path)

    shutil.move(glob.glob('.one/.temp/*')[0], plugin_path)
    shutil.rmtree(TEMP_FOLDER)


def cleanup_plugins(extract_source, installed_plugins):
    if not path.exists(extract_source):
        return

    set_difference = set(os.listdir(extract_source)) - set(installed_plugins.keys())
    list_difference = list(set_difference)
    for directory in list_difference:
        shutil.rmtree(join(extract_source, directory))


def read_plugin_data():
    try:
        with open(PLUGIN_DATA_FILE) as json_file:
            return json.load(json_file)
    except Exception:
        return {}


def check_plugins(extract_source='.one/plugins/'):
    try:
        installed_plugins = {}
        plugin_data = read_plugin_data()

        with open(CONFIG_FILE) as file:
            docs = yaml.load(file, Loader=yaml.BaseLoader)
            for key, url in docs['plugins'].items():
                source = get_config_value('plugins.' + key + '.source')
                plugin_path = join(extract_source, key)
                if not path.exists(plugin_path) or plugin_data[key]['source'] != source:
                    click.echo('Installing plugin %s.' % key)
                    download_plugin(extract_source, source, key)
                    click.echo('Plugin %s successfully installed.\n' % key)

                plugin = {
                    'source': source,
                    'dir': join(extract_source, key)
                }
                installed_plugins[key] = plugin
        file.close()
    except KeyError:
        pass
    except AttributeError:
        click.echo(
            click.style('WARN ', fg='yellow') +
            'Plugin block declared but empty.\n'
        )
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
        raise
    with open(PLUGIN_DATA_FILE, 'w') as outfile:
        json.dump(installed_plugins, outfile)
    cleanup_plugins(extract_source, installed_plugins)


def load_plugins(source='.one/plugins/'):
    if not path.exists('.one'):
        os.mkdir('.one')

    check_plugins()

    if path.exists(source):
        sys.path.append('.one')
        for directory in glob.glob(join(source, '*/')):
            if path.exists(directory + '__init__.py'):
                command_path = '.'.join(directory.rsplit('/', 3)[1:])[:-1] + '.__init__'
                getattr(importlib.import_module(command_path), '__init__')()
