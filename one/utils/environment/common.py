import configparser
from one.__init__ import CLI_ROOT


def get_config(file: str):
    config = configparser.ConfigParser()
    config.read(CLI_ROOT + file)

    return config


def get_credentials_file():
    credentials_file = get_config('/credentials')
    return credentials_file


def get_config_file():
    config_file = get_config('/config')
    return config_file


def get_idp_file():
    idp_file = get_config('/idp')
    return idp_file


def write_config(config, file: str):
    with open(CLI_ROOT + file, 'w+') as configfile:
        config.write(configfile)


def create_secrets(credential, path):
    file = ''
    for key, value in credential.items():
        file += '%s=%s\n' % (key, value)

    with open(path, 'w+') as f:
        f.write(file)
        f.close()
