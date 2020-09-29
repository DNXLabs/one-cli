## Install with PyPi

[PyPI Project](https://pypi.org/project/one-cli)
```bash
pip3 install one-cli

# or setting a version

pip3 install one-cli==<version>
```

## Binary

```
curl -sSL https://raw.githubusercontent.com/DNXLabs/one-cli/master/get_one.sh | bash
```


## Install specific version

```bash
export ONE_VERSION=<version>

# Linux
sudo curl -L https://github.com/DNXLabs/one-cli/releases/download/$ONE_VERSION/one_linux_amd64 -o /usr/local/bin/one
# Macos
sudo curl -L https://github.com/DNXLabs/one-cli/releases/download/$ONE_VERSION/one_macos_amd64 -o /usr/local/bin/one

sudo chmod +x /usr/local/bin/one
```

## Shell completion (Optional)

```
curl -sSL https://raw.githubusercontent.com/DNXLabs/one-cli/master/shell_completion.py | python3
```