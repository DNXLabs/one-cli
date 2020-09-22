# one-cli

CLI to manage all stacks from DNX.

![Build](https://github.com/DNXLabs/one-cli/workflows/Build/badge.svg)
[![PyPI](https://badge.fury.io/py/one-cli.svg)](https://pypi.python.org/pypi/one-cli/)
[![LICENSE](https://img.shields.io/github/license/DNXLabs/one-cli)](https://github.com/DNXLabs/one-cli/blob/master/LICENSE)

## Quick start

1. Download the latest release with the command.
```
curl -sSL https://raw.githubusercontent.com/DNXLabs/one-cli/master/get_one.sh | bash
```

2. Test to ensure the version you installed is up-to-date.
```
one --version
```

3. Install shell completion (Optional)
```
curl -sSL https://raw.githubusercontent.com/DNXLabs/one-cli/master/shell_completion.py | python3
```

#### Install specific version

```bash
export ONE_VERSION=<version>

# Linux
sudo curl -L https://github.com/DNXLabs/one-cli/releases/download/$ONE_VERSION/one_linux_amd64 -o /usr/local/bin/one
# Macos
sudo curl -L https://github.com/DNXLabs/one-cli/releases/download/$ONE_VERSION/one_macos_amd64 -o /usr/local/bin/one

sudo chmod +x /usr/local/bin/one
```

#### Install with PyPi

[PyPI Project](https://pypi.org/project/one-cli)
```bash
pip3 install one-cli

# or setting a version

pip3 install one-cli==<version>
```

##  CI/CD pipelines with Docker

To use the CLI within any CI/CD pipeline we encourage to use our docker image:

[dnxsolutions/one-cli](https://hub.docker.com/repository/docker/dnxsolutions/one-cli)

> WARNING: This docker image should only be used inside CI/CD pipelines and it can generate error if used as an alias.


## Usage
```
Usage: one [OPTIONS] COMMAND [ARGS]...

  CLI to manage all stacks from DNX.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  app        Group of app commands wrapped inside docker.
  auth       Group of auth commands.
  aws        AWS CLI alias.
  aws-v2     AWS v2 CLI alias.
  init       Create config file for CLI in current directory.
  terraform  Group of terraform commands wrapped inside docker.
  workspace  Manage workspaces.
```

#### Running

```bash
$ one my_plugin
It works!
```

## Development

#### Dependencies

- Python 3

#### Python Virtual Environment

```bash
# Create environment
python3 -m venv env

# To activate the environment
source env/bin/activate

# When you finish you can exit typing
deactivate
```

#### Install dependencies

```bash
pip3 install --editable .
```

## Author

Managed by [DNX Solutions](https://github.com/DNXLabs).

## License

Apache 2 Licensed. See [LICENSE](https://github.com/DNXLabs/one-cli/blob/master/LICENSE) for full details.