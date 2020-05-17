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
  update     Update CLI moving to latest stable version.
  workspace  Manage workspaces.
```

## Configuration Example
one.yaml
```yaml
images:
    terraform: dnxsolutions/terraform:0.12.20-dnx1
    gsuite: dnxsolutions/aws-google-auth:latest
    azure: dnxsolutions/docker-aws-azure-ad:latest
workspaces:
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

## Author
Managed by DNX Solutions.

## License
Apache 2 Licensed. See [LICENSE](https://github.com/DNXLabs/one-cli/blob/master/LICENSE) for full details.