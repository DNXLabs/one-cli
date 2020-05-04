# ONE

CLI to manage all stacks from DNX.

![Build](https://github.com/DNXLabs/one-cli/workflows/Build/badge.svg)
[![LICENSE](https://img.shields.io/github/license/DNXLabs/one-cli)](https://github.com/DNXLabs/one-cli/blob/master/LICENSE)

## Quick start
Use everything you need from DNX in 4 steps.

1. Download the latest release with the command.
```
# linux
curl -L https://github.com/DNXLabs/one-cli/releases/latest/download/one_linux_amd64 -o one

# macos
curl -L https://github.com/DNXLabs/one-cli/releases/latest/download/one_macos_amd64 -o one
```

2. Make the one binary executable.
```
chmod +x ./one
```

3. Move the binary in to your PATH.
```
sudo mv ./one /usr/local/bin/one
```

4. Test to ensure the version you installed is up-to-date.
```
one --version
```

## Usage
```
Usage: one [OPTIONS] COMMAND [ARGS]...

  CLI to manage all stacks from DNX.

Options:
  --help  Show this message and exit.

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
    terraform: dnxsolutions/terraform:0.12.20-dnx1
    gsuite: dnxsolutions/aws-google-auth:latest
    azure: dnxsolutions/docker-aws-azure-ad:latest
workspaces:
    - mgmt:
        aws-account-id:
        aws-role:
        workspace:
    - nonprod:
        aws-account-id:
        aws-role:
        workspace:
    - prod:
        aws-account-id:
        aws-role:
        workspace:
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