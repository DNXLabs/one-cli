# one-cli

CLI to manage all stacks from DNX.

![Build](https://github.com/DNXLabs/one-cli/workflows/Build/badge.svg)
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

## Running with Docker
To easy start with docker just add this line to your `bash profile`.
```bash
alias one='docker run -it -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/root -v $HOME/.one:/root/.one dnxsolutions/one-cli'
```

Or if you want to run the script by yourself, here we have one example:
```bash
docker run -it -v /var/run/docker.sock:/var/run/docker.sock \
               -v $HOME/.one:/root/.one \
               --entrypoint /bin/bash \
               dnxsolutions/one-cli
```

## Usage
```
Usage: one [OPTIONS] COMMAND [ARGS]...

  CLI to manage all stacks from DNX.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  idp        Manage the IDP configuration in your local.
  login      Group of commands to login specifying one SSO provider.
  terraform  Group of terraform commands wrapped inside docker.
  workspace  Manage workspaces.
```

## Configuration Example
one.yaml
```yaml
images:
  terraform: dnxsolutions/terraform:0.12.24-dnx1
  gsuite: dnxsolutions/aws-google-auth:latest
  azure: dnxsolutions/docker-aws-azure-ad:latest
  aws: dnxsolutions/aws:1.18.44-dnx2
  ecs-deploy: dnxsolutions/ecs-deploy:1.2.0

app:
  name: copacabana
  port: 80
  docker:
    file: Dockerfile
    image-name: copacabana
    registry-type: ecr
    registry-options:
      ecr-aws-account-id: <redact>
      ecr-aws-region: ap-southeast-2
      ecr-aws-assume-role: true
      ecr-aws-role: <redact>
  ecs-task-definition-file: task-definition.tpl.json

workspaces:
  mgmt-app:
    type: ecs
    aws-account-id: <redact>
    aws-role: <redact>
    aws-assume-role: true|false
    aws-region: ap-southeast-2
    ecs-cluster-name: cluster-01
  mgmt:
    aws-account-id:
    aws-role:
  nonprod:
    aws-account-id:
    aws-role:
  prod:
    aws-account-id:
    aws-role:
  default:
    aws-account-id:
    aws-role:
    aws-assume-role: true|false
```

## Setup

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
pip3 install -r requirements.txt
pip3 install --editable .
```

#### Manualy generate binary
```bash
pyinstaller --clean --hidden-import one.__main__ cli.py --onefile --noconsole -n one
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
    print('It works!')
```

#### Running
```bash
$ one my_plugin
It works!
```

## Author
Managed by DNX Solutions.

## License
Apache 2 Licensed. See [LICENSE](https://github.com/DNXLabs/one-cli/blob/master/LICENSE) for full details.