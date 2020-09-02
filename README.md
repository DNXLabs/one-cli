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

## Configuration Example

one.yaml
```yaml
images:
  terraform: dnxsolutions/terraform:0.13.0-dnx1
  gsuite: dnxsolutions/aws-google-auth:latest
  azure: dnxsolutions/docker-aws-azure-ad:latest
  aws: dnxsolutions/aws:1.18.44-dnx2
  aws_2: dnxsolutions/aws:2.0.37-dnx1
  ecs_deploy: dnxsolutions/ecs-deploy:1.2.0

required_version: ">= 0.5.0, <= 0.7.0"

# ECS App
app:
  name: copacabana
  port: 80
  docker:
    file: Dockerfile
    image_name: copacabana
    registry_type: ecr
    registry_options:
      ecr_aws_account_id: <redact>
      ecr_aws_region: ap-southeast-2
      ecr_aws_assume_role: true
      ecr_aws_role: <redact>
  ecs_task_definition_file: task-definition.tpl.json

# Static App
app:
  type: static
  src: ./build
  s3_bucket_name: <redact>
  distribution_id: <redact>

workspaces:

  # ECS App example:
  mgmt_ecs_app:
    type: ecs
    aws:
      account_id: <redact>
      role: <redact>
      assume_role: true|false (default to false)
      region: ap-southeast-2
    ecs_cluster_name: cluster-01

  # Static App example:
  mgmt_static_app:
    aws:
      account_id: <redact>
      role: <redact>
      region: ap-southeast-2
      assume_role: true
    # Override the template static app
    app:
      src: ./build
      s3_bucket_name: <redact>
      distribution_id: <redact>

  # Terraform example
  mgmt:
    aws:
      account_id: <redact>
      role: <redact>
  nonprod:
    aws:
      account_id: <redact>
      role: <redact>
  prod:
    aws:
      account_id: <redact>
      role: <redact>
  default:
    aws:
      account_id: <redact>
      role: <redact>
      assume_role: true|false (default to false)
```

## Plugin System

To give better support for customization inside the CLI we created a `plugin system` that you can extend code, creating new commands and groups and even modify the existing ones.

All plugins need to be created inside ` ~/.one/plugins/*`

#### Folder Structure

```bash
└── plugins
    ├── __init__.py (empty file)
    └── my_plugin.py
```

#### Plugin Example

`~/.one/plugins/my_plugin.py`
```python
import click
from one.one import cli


def __init__():
    cli.add_command(my_plugin)


@click.command(name='my_plugin', help='My plugin command')
def my_plugin():
    click.echo('It works!')
```

#### Running

```bash
$ one my_plugin
It works!
```

#### Manualy generate binary

```bash
pip install pyinstaller
pyinstaller --clean --hidden-import one.__main__ cli.py --onefile --noconsole -n one
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